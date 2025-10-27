"""
Interactive menu for AXE CLI
Provides a user-friendly menu interface for all operations
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

from .converter import ArxivConverter
from .ui_constants import console, get_panel_style, get_text_style, get_border_style, TABLE_STYLES, get_styled_title


class InteractiveMenu:
    """Interactive menu interface for AXE CLI"""
    
    def __init__(self, config, stats_manager):
        """Initialize interactive menu
        
        Args:
            config: Config instance
            stats_manager: StatsManager instance
        """
        self.config = config
        self.stats_manager = stats_manager
        self.converter = ArxivConverter(stats_manager)
        self.running = True
    
    def run(self):
        """Run the interactive menu loop"""
        self._show_welcome()
        
        while self.running:
            try:
                self._show_menu()
                choice = self._get_choice()
                self._handle_choice(choice)
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Operation cancelled[/bold yellow]")
                if Confirm.ask("Exit AXE CLI?", default=True):
                    self.running = False
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        
        self._show_goodbye()
    
    def _show_welcome(self):
        """Display welcome banner"""
        banner = Text()
        banner.append("  AXE ", style="bold red")
        banner.append("AXE CLI", style="bold cyan")
        banner.append(" - ArXiv Extraction Tool\n", style="bold white")
        banner.append("  Interactive Mode", style="dim")
        
        console.print()
        console.print(Panel.fit(
            banner,
            **get_panel_style('secondary')
        ))
        console.print()
    
    def _show_menu(self):
        """Display main menu"""
        table = Table(**TABLE_STYLES['compact'])
        table.add_column("Option", style=get_text_style('title'), width=8)
        table.add_column("Description", style=get_text_style('body'))
        
        table.add_row("1", "Chop files (convert arXiv papers)")
        table.add_row("2", "Configure paths")
        table.add_row("3", "View statistics")
        table.add_row("4", "Help & Documentation")
        table.add_row("5", "Exit")
        
        console.print()
        console.print(Panel.fit(
            table,
            title=get_styled_title("Main Menu", "primary"),
            **get_panel_style('primary')
        ))
        console.print()
    
    def _get_choice(self) -> str:
        """Get user menu choice
        
        Returns:
            User's choice as string
        """
        return Prompt.ask(
            f"[{get_text_style('title')}]Choose an option[/{get_text_style('title')}]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )
    
    def _handle_choice(self, choice: str):
        """Handle user's menu choice
        
        Args:
            choice: User's choice
        """
        if choice == "1":
            self._chop_menu()
        elif choice == "2":
            self._path_menu()
        elif choice == "3":
            self._stats_menu()
        elif choice == "4":
            self._help_menu()
        elif choice == "5":
            self.running = False
    
    def _chop_menu(self):
        """Handle chop (conversion) menu"""
        console.print()
        console.print(Panel.fit(
            "[bold]Chop Operation - Convert arXiv Papers[/bold]\n\n"
            "[cyan]1.[/cyan] Process current directory\n"
            "[cyan]2.[/cyan] Process configured path\n"
            "[cyan]3.[/cyan] Process specific file/directory\n"
            "[cyan]4.[/cyan] Process arXiv URL\n"
            "[cyan]5.[/cyan] Back to main menu",
            title=get_styled_title("Chop Operation", "success"),
            **get_panel_style('success')
        ))
        console.print()
        
        choice = Prompt.ask(
            "Choose operation",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )
        
        if choice == "5":
            return
        
        # Get output format
        format_choice = Prompt.ask(
            "Output format",
            choices=["text", "markdown", "both"],
            default="markdown"
        )
        
        # Get output directory
        output_dir = Path(self.config.get('output_path', Path.cwd() / 'axe_output'))
        custom_output = Confirm.ask(
            f"Use default output path? ({output_dir})",
            default=True
        )
        
        if not custom_output:
            output_path = Prompt.ask("Enter output directory path")
            output_dir = Path(output_path).resolve()
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process based on choice
        try:
            if choice == "1":
                input_dir = Path.cwd()
                console.print(f"\n[bold]Processing:[/bold] {input_dir}")
                self.converter.process_directory(input_dir, output_dir, format_choice)
            
            elif choice == "2":
                input_dir = Path(self.config.get('input_path', Path.cwd()))
                console.print(f"\n[bold]Processing:[/bold] {input_dir}")
                self.converter.process_directory(input_dir, output_dir, format_choice)
            
            elif choice == "3":
                path = Prompt.ask("Enter file or directory path")
                input_path = Path(path).resolve()
                
                if not input_path.exists():
                    console.print(f"[bold red]Error:[/bold red] Path does not exist: {input_path}")
                    return
                
                if input_path.is_file():
                    self.converter.process_file(input_path, output_dir, format_choice)
                elif input_path.is_dir():
                    self.converter.process_directory(input_path, output_dir, format_choice)
            
            elif choice == "4":
                url = Prompt.ask("Enter arXiv URL or ID")
                self.converter.process_url(url, output_dir, format_choice)
            
            # Show run statistics
            self.stats_manager.show_run_stats()
            
            # Save persistent statistics
            self.stats_manager.save_persistent_stats()
            
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
    
    def _path_menu(self):
        """Handle path configuration menu"""
        console.print()
        console.print(Panel.fit(
            "[bold]Path Configuration[/bold]\n\n"
            "[cyan]1.[/cyan] Set input path\n"
            "[cyan]2.[/cyan] Set output path\n"
            "[cyan]3.[/cyan] View current paths\n"
            "[cyan]4.[/cyan] Reset to defaults\n"
            "[cyan]5.[/cyan] Back to main menu",
            title=get_styled_title("Path Configuration", "warning"),
            **get_panel_style('warning')
        ))
        console.print()
        
        choice = Prompt.ask(
            "Choose operation",
            choices=["1", "2", "3", "4", "5"],
            default="3"
        )
        
        if choice == "1":
            path = Prompt.ask("Enter input directory path", default=str(Path.cwd()))
            path_obj = Path(path).resolve()
            
            if not path_obj.exists():
                console.print(f"[bold red]Error:[/bold red] Path does not exist: {path_obj}")
                return
            
            if not path_obj.is_dir():
                console.print(f"[bold red]Error:[/bold red] Path must be a directory")
                return
            
            self.config.set('input_path', str(path_obj))
            console.print(f"[bold green][/bold green] Input path set to: [cyan]{path_obj}[/cyan]")
        
        elif choice == "2":
            path = Prompt.ask("Enter output directory path", default=str(Path.cwd() / 'axe_output'))
            path_obj = Path(path).resolve()
            path_obj.mkdir(parents=True, exist_ok=True)
            
            self.config.set('output_path', str(path_obj))
            console.print(f"[bold green][/bold green] Output path set to: [cyan]{path_obj}[/cyan]")
        
        elif choice == "3":
            current_in = self.config.get('input_path', Path.cwd())
            current_out = self.config.get('output_path', Path.cwd() / 'axe_output')
            
            console.print()
            console.print(Panel.fit(
                f"[bold cyan]Input Path:[/bold cyan]\n{current_in}\n\n"
                f"[bold green]Output Path:[/bold green]\n{current_out}",
                title=get_styled_title("Current Paths", "primary"),
                **get_panel_style('primary')
            ))
        
        elif choice == "4":
            if Confirm.ask("Reset paths to defaults?", default=False):
                self.config.set('input_path', str(Path.cwd()))
                self.config.set('output_path', str(Path.cwd() / 'axe_output'))
                console.print("[bold green][/bold green] Paths reset to defaults")
    
    def _stats_menu(self):
        """Handle statistics menu"""
        console.print()
        console.print(Panel.fit(
            "[bold]Statistics[/bold]\n\n"
            "[cyan]1.[/cyan] View persistent statistics\n"
            "[cyan]2.[/cyan] Reset statistics\n"
            "[cyan]3.[/cyan] Back to main menu",
            title=get_styled_title("Statistics", "info"),
            **get_panel_style('info')
        ))
        console.print()
        
        choice = Prompt.ask(
            "Choose operation",
            choices=["1", "2", "3"],
            default="1"
        )
        
        if choice == "1":
            self.stats_manager.show_persistent_stats()
        
        elif choice == "2":
            if Confirm.ask("Are you sure you want to reset all statistics?", default=False):
                self.stats_manager.reset_persistent_stats()
                console.print("[bold green][/bold green] Statistics reset successfully")
    
    def _help_menu(self):
        """Display help information"""
        console.print()
        console.print(Panel.fit(
            "[bold cyan]AXE CLI - Help & Documentation[/bold cyan]\n\n"
            "[bold]Quick Start:[/bold]\n"
            "  1. Use [cyan]Chop[/cyan] menu to convert papers\n"
            "  2. Configure paths for default directories\n"
            "  3. View statistics to track your progress\n\n"
            "[bold]Direct Commands:[/bold]\n"
            "  [yellow]axe chop .[/yellow]              Process current directory\n"
            "  [yellow]axe chop path[/yellow]          Process configured path\n"
            "  [yellow]axe chop <file>[/yellow]        Process single file\n"
            "  [yellow]axe path --in <dir>[/yellow]    Set input directory\n"
            "  [yellow]axe path --out <dir>[/yellow]   Set output directory\n"
            "  [yellow]axe stats --show[/yellow]       Show statistics\n\n"
            "[bold]Supported Formats:[/bold]\n"
            "  • PDF files from arXiv\n"
            "  • arXiv URLs (abs or pdf)\n"
            "  • arXiv IDs (e.g., 2103.15538)\n\n"
            "[bold]Output Formats:[/bold]\n"
            "  • Text (.txt)\n"
            "  • Markdown (.md)\n"
            "  • Both formats\n\n"
            "Press Enter to continue...",
            title=get_styled_title("Help & Documentation", "primary"),
            **get_panel_style('primary')
        ))
        
        input()
    
    def _show_goodbye(self):
        """Display goodbye message"""
        console.print()
        console.print(Panel.fit(
            "[bold green]Thank you for using AXE CLI![/bold green]\n"
            "Your configuration and statistics have been saved.",
            title=get_styled_title("Goodbye", "success"),
            **get_panel_style('success')
        ))
        console.print()