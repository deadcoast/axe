"""
Syntax Highlighting Integration for AXE CLI
Implements Phase 3 features: syntax highlighting, markdown rendering, and code block themes
Following mech_god balance system: feature(a:feat) + minimal(a:miml) = balance(a:bal)
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from .ui_constants import console, get_panel_style, get_text_style


class SyntaxHighlighter:
    """Enhanced syntax highlighting with multiple language support"""

    def __init__(self):
        """Initialize syntax highlighter"""
        self.language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".h": "c",
            ".hpp": "cpp",
            ".cs": "csharp",
            ".php": "php",
            ".rb": "ruby",
            ".go": "go",
            ".rs": "rust",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".r": "r",
            ".m": "matlab",
            ".sh": "bash",
            ".bash": "bash",
            ".zsh": "bash",
            ".fish": "fish",
            ".ps1": "powershell",
            ".sql": "sql",
            ".html": "html",
            ".htm": "html",
            ".xml": "xml",
            ".css": "css",
            ".scss": "scss",
            ".sass": "sass",
            ".less": "less",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".ini": "ini",
            ".cfg": "ini",
            ".conf": "ini",
            ".md": "markdown",
            ".tex": "latex",
            ".rst": "rst",
            ".txt": "text",
            ".log": "text",
            ".csv": "csv",
            ".tsv": "csv",
        }

        # Code block themes
        self.themes = {
            "default": "monokai",
            "light": "github",
            "dark": "monokai",
            "minimal": "default",
            "colorful": "rainbow_dash",
        }

    def detect_language(self, file_path: Path, content: Optional[str] = None) -> str:
        """Detect programming language from file path or content

        Args:
            file_path: Path to the file
            content: Optional file content for detection

        Returns:
            Detected language name
        """
        # First try file extension
        if file_path.suffix.lower() in self.language_map:
            return self.language_map[file_path.suffix.lower()]

        # Try to detect from content if available
        if content:
            # Check for shebang
            shebang_match = re.match(r"^#!.*?/(\w+)", content)
            if shebang_match:
                interpreter = shebang_match.group(1)
                if interpreter in ["python", "python3", "python2"]:
                    return "python"
                elif interpreter in ["bash", "sh", "zsh", "fish"]:
                    return "bash"
                elif interpreter == "node":
                    return "javascript"

            # Check for common patterns
            if re.search(r"<\?php", content):
                return "php"
            elif re.search(r"<html|<head|<body", content, re.IGNORECASE):
                return "html"
            elif re.search(r"@\w+\s*\(", content):
                return "python"  # Likely Python decorator
            elif re.search(r"function\s+\w+\s*\(", content):
                return "javascript"
            elif re.search(r"public\s+class\s+\w+", content):
                return "java"
            elif re.search(r"#include\s*<", content):
                return "cpp"

        return "text"

    def highlight_code(
        self,
        content: str,
        language: str = "text",
        theme: str = "default",
        line_numbers: bool = True,
    ) -> Syntax:
        """Create syntax highlighted code

        Args:
            content: Code content to highlight
            language: Programming language
            theme: Color theme
            line_numbers: Show line numbers

        Returns:
            Syntax object for display
        """
        theme_name = self.themes.get(theme, "monokai")

        return Syntax(
            content,
            language,
            theme=theme_name,
            line_numbers=line_numbers,
            word_wrap=True,
            background_color="default",
        )

    def highlight_file(
        self, file_path: Path, theme: str = "default", line_numbers: bool = True
    ) -> Optional[Syntax]:
        """Highlight a file's content

        Args:
            file_path: Path to the file
            theme: Color theme
            line_numbers: Show line numbers

        Returns:
            Syntax object or None if file cannot be read
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            language = self.detect_language(file_path, content)
            return self.highlight_code(content, language, theme, line_numbers)

        except (IOError, UnicodeDecodeError) as e:
            console.print(f"[bold red]Error reading file {file_path}:[/bold red] {e}")
            return None

    def display_code_block(
        self,
        content: str,
        language: str = "text",
        title: str = "",
        theme: str = "default",
    ):
        """Display a code block with syntax highlighting

        Args:
            content: Code content
            language: Programming language
            title: Optional title
            theme: Color theme
        """
        syntax = self.highlight_code(content, language, theme)

        if title:
            console.print()
            console.print(
                Panel.fit(
                    syntax, title=f"[bold]{title}[/bold]", **get_panel_style("primary")
                )
            )
        else:
            console.print(syntax)

    def display_file(
        self, file_path: Path, theme: str = "default", title: Optional[str] = None
    ):
        """Display a file with syntax highlighting

        Args:
            file_path: Path to the file
            theme: Color theme
            title: Optional title (defaults to filename)
        """
        syntax = self.highlight_file(file_path, theme)

        if syntax:
            display_title = title or file_path.name
            console.print()
            console.print(
                Panel.fit(
                    syntax,
                    title=f"[bold]{display_title}[/bold]",
                    **get_panel_style("primary"),
                )
            )
            console.print()


class MarkdownRenderer:
    """Enhanced markdown rendering with syntax highlighting"""

    def __init__(self, syntax_highlighter: SyntaxHighlighter):
        """Initialize markdown renderer

        Args:
            syntax_highlighter: SyntaxHighlighter instance
        """
        self.syntax_highlighter = syntax_highlighter

    def render_markdown(self, content: str, theme: str = "default") -> Markdown:
        """Render markdown content with syntax highlighting

        Args:
            content: Markdown content
            theme: Color theme for code blocks

        Returns:
            Markdown object for display
        """
        # Pre-process code blocks to ensure proper syntax highlighting
        processed_content = self._process_code_blocks(content, theme)

        return Markdown(processed_content)

    def _process_code_blocks(self, content: str, theme: str) -> str:
        """Process markdown code blocks for enhanced syntax highlighting

        Args:
            content: Markdown content
            theme: Color theme

        Returns:
            Processed markdown content
        """
        # Pattern for fenced code blocks
        code_block_pattern = r"```(\w+)?\n(.*?)```"

        def replace_code_block(match):
            language = match.group(1) or "text"
            code_content = match.group(2)

            # Create syntax highlighted version
            syntax = self.syntax_highlighter.highlight_code(
                code_content, language, theme
            )

            # For now, return the original block (Rich Markdown handles syntax highlighting)
            return match.group(0)

        return re.sub(code_block_pattern, replace_code_block, content, flags=re.DOTALL)

    def display_markdown(self, content: str, title: str = "", theme: str = "default"):
        """Display markdown content with enhanced rendering

        Args:
            content: Markdown content
            title: Optional title
            theme: Color theme
        """
        markdown = self.render_markdown(content, theme)

        if title:
            console.print()
            console.print(
                Panel.fit(
                    markdown,
                    title=f"[bold]{title}[/bold]",
                    **get_panel_style("primary"),
                )
            )
        else:
            console.print(markdown)

    def display_markdown_file(self, file_path: Path, theme: str = "default"):
        """Display a markdown file with enhanced rendering

        Args:
            file_path: Path to markdown file
            theme: Color theme
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.display_markdown(content, file_path.name, theme)

        except (IOError, UnicodeDecodeError) as e:
            console.print(
                f"[bold red]Error reading markdown file {file_path}:[/bold red] {e}"
            )


class CodeBlockThemes:
    """Code block theme management"""

    def __init__(self):
        """Initialize theme manager"""
        self.available_themes = {
            "default": "monokai",
            "light": "github",
            "dark": "monokai",
            "minimal": "default",
            "colorful": "rainbow_dash",
            "ocean": "ocean",
            "solarized": "solarized-dark",
            "dracula": "dracula",
            "nord": "nord",
        }

    def get_theme(self, theme_name: str) -> str:
        """Get theme name for Rich Syntax

        Args:
            theme_name: Theme identifier

        Returns:
            Rich theme name
        """
        return self.available_themes.get(theme_name, "monokai")

    def list_themes(self) -> Dict[str, str]:
        """List available themes

        Returns:
            Dictionary of theme names and descriptions
        """
        return {
            "default": "Default dark theme (monokai)",
            "light": "Light theme (github)",
            "dark": "Dark theme (monokai)",
            "minimal": "Minimal theme (default)",
            "colorful": "Colorful theme (rainbow_dash)",
            "ocean": "Ocean theme",
            "solarized": "Solarized dark theme",
            "dracula": "Dracula theme",
            "nord": "Nord theme",
        }

    def display_theme_preview(self, theme_name: str):
        """Display a preview of a theme

        Args:
            theme_name: Theme to preview
        """
        sample_code = '''def hello_world():
    """A simple hello world function"""
    print("Hello, World!")
    return True

class Example:
    def __init__(self):
        self.value = 42
    
    def calculate(self, x: int) -> int:
        return self.value + x
'''

        syntax_highlighter = SyntaxHighlighter()
        syntax = syntax_highlighter.highlight_code(sample_code, "python", theme_name)

        console.print()
        console.print(
            Panel.fit(
                syntax,
                title=f"[bold]{theme_name.title()} Theme Preview[/bold]",
                **get_panel_style("primary"),
            )
        )
        console.print()


# Global instances for easy access
syntax_highlighter = SyntaxHighlighter()
markdown_renderer = MarkdownRenderer(syntax_highlighter)
theme_manager = CodeBlockThemes()


def show_syntax_highlighting_demo():
    """Display a demo of syntax highlighting capabilities"""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Syntax Highlighting Demo[/bold cyan]\n\n"
            "This demonstrates the enhanced syntax highlighting capabilities:\n"
            "• Automatic language detection\n"
            "• Multiple color themes\n"
            "• Code block rendering\n"
            "• Markdown integration\n\n"
            "Available themes: default, light, dark, minimal, colorful, ocean, solarized, dracula, nord",
            title="[bold]Syntax Highlighting Features[/bold]",
            **get_panel_style("info"),
        )
    )

    # Show theme preview
    theme_manager.display_theme_preview("default")


if __name__ == "__main__":
    # Demo syntax highlighting
    show_syntax_highlighting_demo()

    # Show available themes
    themes = theme_manager.list_themes()
    console.print()
    console.print(
        Panel.fit(
            "\n".join(
                [f"[cyan]{name}[/cyan]: {desc}" for name, desc in themes.items()]
            ),
            title="[bold]Available Themes[/bold]",
            **get_panel_style("primary"),
        )
    )
