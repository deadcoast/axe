"""
ArXiv paper converter
Handles downloading and converting arXiv papers to text/markdown
"""

import re
import time
from pathlib import Path
from typing import Optional
import arxiv
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.panel import Panel

from .ui_constants import console, PROGRESS_STYLES, STATUS_STYLES
from .ui_advanced import progress_manager, visual_feedback


class ArxivConverter:
    """Handles conversion of arXiv papers to text/markdown"""

    def __init__(self, stats_manager):
        """Initialize converter

        Args:
            stats_manager: StatsManager instance for tracking statistics
        """
        self.stats_manager = stats_manager
        self.client = arxiv.Client()

    def extract_arxiv_id(self, text: str) -> Optional[str]:
        """Extract arXiv ID from various formats

        Args:
            text: Text that may contain arXiv ID (URL, filename, or plain ID)

        Returns:
            arXiv ID or None
        """
        # Pattern for arXiv IDs (old and new format)
        patterns = [
            r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)",  # URL format
            r"(\d{4}\.\d{4,5}(?:v\d+)?)",  # Direct ID
            r"arxiv[:\-\s]*(\d{4}\.\d{4,5}(?:v\d+)?)",  # Various prefixed formats
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def process_file(self, file_path: Path, output_dir: Path, format: str):
        """Process a single file

        Args:
            file_path: Path to the file
            output_dir: Output directory
            format: Output format (text, markdown, or both)
        """
        console.print(f"[bold]Processing:[/bold] [cyan]{file_path.name}[/cyan]")

        try:
            # Check if it's a PDF
            if file_path.suffix.lower() == ".pdf":
                self._convert_pdf(file_path, output_dir, format)
            else:
                # Try to extract arXiv ID from filename
                arxiv_id = self.extract_arxiv_id(file_path.stem)
                if arxiv_id:
                    self._download_and_convert(arxiv_id, output_dir, format)
                else:
                    console.print(
                        f"[yellow]Skipped:[/yellow] Not a PDF or recognizable arXiv file: {file_path.name}"
                    )
                    self.stats_manager.increment_skipped()

        except Exception as e:
            console.print(
                f"[bold red]Error processing {file_path.name}:[/bold red] {str(e)}"
            )
            self.stats_manager.increment_failed()

    def process_directory(self, dir_path: Path, output_dir: Path, format: str):
        """Process all eligible files in a directory

        Args:
            dir_path: Directory path
            output_dir: Output directory
            format: Output format (text, markdown, or both)
        """
        # Find all PDFs and potential arXiv files
        pdf_files = list(dir_path.glob("*.pdf"))

        if not pdf_files:
            console.print(f"[yellow]No PDF files found in:[/yellow] {dir_path}")
            return

        console.print(f"[bold]Found {len(pdf_files)} PDF file(s) to process[/bold]\n")

        # Use advanced progress manager
        progress = progress_manager.create_file_progress(
            len(pdf_files), "file_processing"
        )

        with progress:
            for i, pdf_file in enumerate(pdf_files):
                progress_manager.update_progress(
                    "file_processing", description=f"[cyan]Processing: {pdf_file.name}"
                )
                self.process_file(pdf_file, output_dir, format)
                progress_manager.update_progress("file_processing", advance=1)
                time.sleep(0.1)  # Brief pause to avoid rate limiting

        progress_manager.finish_progress("file_processing")

    def process_url(self, url: str, output_dir: Path, format: str):
        """Process an arXiv URL

        Args:
            url: arXiv URL
            output_dir: Output directory
            format: Output format (text, markdown, or both)
        """
        arxiv_id = self.extract_arxiv_id(url)

        if not arxiv_id:
            console.print(
                f"[bold red]Error:[/bold red] Could not extract arXiv ID from URL: {url}"
            )
            self.stats_manager.increment_failed()
            return

        console.print(f"[bold]Processing arXiv ID:[/bold] [cyan]{arxiv_id}[/cyan]")
        self._download_and_convert(arxiv_id, output_dir, format)

    def _download_and_convert(self, arxiv_id: str, output_dir: Path, format: str):
        """Download arXiv paper and convert it

        Args:
            arxiv_id: arXiv paper ID
            output_dir: Output directory
            format: Output format (text, markdown, or both)
        """
        try:
            # Search for the paper
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(self.client.results(search), None)

            if not paper:
                console.print(
                    f"[bold red]Error:[/bold red] Could not find paper: {arxiv_id}"
                )
                self.stats_manager.increment_failed()
                return

            # Create safe filename from title
            safe_title = self._sanitize_filename(paper.title)

            # Download PDF
            pdf_path = output_dir / f"{safe_title}.pdf"

            # Use visual feedback system for download
            download_status = visual_feedback.show_loading_status(
                f"[bold green]Downloading {arxiv_id}...",
                "download",
                STATUS_STYLES["loading"]["spinner_style"],
            )

            try:
                paper.download_pdf(
                    dirpath=str(output_dir), filename=f"{safe_title}.pdf"
                )
                visual_feedback.stop_loading_status("download")
                visual_feedback.show_success_message(
                    f"Downloaded: {safe_title}.pdf", f"arXiv ID: {arxiv_id}"
                )
            except Exception as e:
                visual_feedback.stop_loading_status("download")
                visual_feedback.show_error_message(
                    f"Failed to download {arxiv_id}", str(e)
                )
                raise

            # Convert to requested format(s)
            arxiv_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            self._convert_pdf(
                pdf_path,
                output_dir,
                format,
                paper_title=safe_title,
                arxiv_url=arxiv_url,
            )

        except StopIteration:
            console.print(f"[bold red]Error:[/bold red] Paper not found: {arxiv_id}")
            self.stats_manager.increment_failed()
        except Exception as e:
            console.print(
                f"[bold red]Error downloading/converting {arxiv_id}:[/bold red] {str(e)}"
            )
            self.stats_manager.increment_failed()

    def _convert_pdf(
        self,
        pdf_path: Path,
        output_dir: Path,
        format: str,
        paper_title: Optional[str] = None,
        arxiv_url: Optional[str] = None,
    ):
        """Convert PDF to text/markdown using arxiv2text

        Args:
            pdf_path: Path to PDF file
            output_dir: Output directory
            format: Output format (text, markdown, or both)
            paper_title: Optional paper title for filename
            arxiv_url: Original arXiv URL for conversion
        """
        try:
            from arxiv2text import arxiv_to_text, arxiv_to_md

            base_name = paper_title or pdf_path.stem

            # Use the original arXiv URL if available, otherwise try the local file
            if arxiv_url:
                conversion_url = arxiv_url
            else:
                conversion_url = pdf_path.as_uri()

            if format in ["text", "both"]:
                text_status = visual_feedback.show_loading_status(
                    "[bold yellow]Converting to text...",
                    "text_conversion",
                    STATUS_STYLES["loading"]["spinner_style"],
                )

                try:
                    text_content = arxiv_to_text(conversion_url, str(output_dir))

                    # Save text file
                    text_path = output_dir / f"{base_name}.txt"
                    with open(text_path, "w", encoding="utf-8") as f:
                        f.write(text_content)

                    visual_feedback.stop_loading_status("text_conversion")
                    visual_feedback.show_success_message(f"Created: {text_path.name}")
                except Exception as e:
                    visual_feedback.stop_loading_status("text_conversion")
                    visual_feedback.show_error_message("Text conversion failed", str(e))
                    raise

            if format in ["markdown", "both"]:
                md_status = visual_feedback.show_loading_status(
                    "[bold yellow]Converting to markdown...",
                    "md_conversion",
                    STATUS_STYLES["loading"]["spinner_style"],
                )

                try:
                    md_content = arxiv_to_md(conversion_url, str(output_dir))

                    # The library may save the file directly, but we'll ensure it's there
                    md_path = output_dir / f"{base_name}.md"
                    if not md_path.exists() and md_content:
                        with open(md_path, "w", encoding="utf-8") as f:
                            f.write(md_content)

                    visual_feedback.stop_loading_status("md_conversion")
                    if md_path.exists():
                        visual_feedback.show_success_message(f"Created: {md_path.name}")
                except Exception as e:
                    visual_feedback.stop_loading_status("md_conversion")
                    visual_feedback.show_error_message(
                        "Markdown conversion failed", str(e)
                    )
                    raise

            self.stats_manager.increment_success()

        except ImportError:
            console.print(
                "[bold red]Error:[/bold red] arxiv2text library not installed"
            )
            console.print("Install with: pip install arxiv2text")
            self.stats_manager.increment_failed()
        except Exception as e:
            console.print(f"[bold red]Conversion error:[/bold red] {str(e)}")
            self.stats_manager.increment_failed()

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename by removing invalid characters

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', "", filename)
        # Replace multiple spaces with single space
        filename = re.sub(r"\s+", " ", filename)
        # Trim and limit length
        filename = filename.strip()[:200]
        return filename
