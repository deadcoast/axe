#!/usr/bin/env python3
"""
AXE CLI - ArXiv Extraction CLI
A powerful CLI tool for downloading and converting arXiv papers
"""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .config import Config
from .converter import ArxivConverter
from .stats import StatsManager
from .interactive import InteractiveMenu

console = Console()
config = Config()
stats_manager = StatsManager()


@click.group(invoke_without_command=True)
@click.pass_context
def axe(ctx):
    """AXE CLI - ArXiv Extraction Command Line Interface
    
    Process arXiv papers with ease. Use interactive mode or direct commands.
    """
    if ctx.invoked_subcommand is None:
        # No subcommand provided - launch interactive menu
        interactive = InteractiveMenu(config, stats_manager)
        interactive.run()


@axe.command()
@click.option('--in', 'input_path', type=click.Path(), help='Set default input directory')
@click.option('--out', 'output_path', type=click.Path(), help='Set default output directory')
@click.option('--show', is_flag=True, help='Show current path configuration')
def path(input_path, output_path, show):
    """Manage input and output directory paths"""
    
    if show:
        # Display current path configuration
        current_in = config.get('input_path', Path.cwd())
        current_out = config.get('output_path', Path.cwd() / 'axe_output')
        
        console.print(Panel.fit(
            f"[bold cyan]Input Path:[/bold cyan] {current_in}\n"
            f"[bold green]Output Path:[/bold green] {current_out}",
            title="[bold]Path Configuration[/bold]",
            border_style="blue"
        ))
        return
    
    if input_path:
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            console.print(f"[bold red]Error:[/bold red] Input path does not exist: {input_path}")
            sys.exit(1)
        if not input_path.is_dir():
            console.print(f"[bold red]Error:[/bold red] Input path must be a directory: {input_path}")
            sys.exit(1)
        
        config.set('input_path', str(input_path))
        console.print(f"[bold green]✓[/bold green] Input path set to: [cyan]{input_path}[/cyan]")
    
    if output_path:
        output_path = Path(output_path).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        
        config.set('output_path', str(output_path))
        console.print(f"[bold green]✓[/bold green] Output path set to: [cyan]{output_path}[/cyan]")
    
    if not input_path and not output_path and not show:
        console.print("[yellow]No options provided. Use --help for usage information.[/yellow]")


@axe.command()
@click.argument('target', required=False, default=None)
@click.option('--format', '-f', type=click.Choice(['text', 'markdown', 'both'], case_sensitive=False), 
              default='markdown', help='Output format (default: markdown)')
@click.option('--out', 'output_dir', type=click.Path(), help='Override output directory for this operation')
def chop(target, format, output_dir):
    """Convert arXiv papers to text/markdown
    
    TARGET can be:
    - A file path (PDF or arXiv URL)
    - A directory path
    - '.' to process current directory
    - 'path' to use configured default path
    """
    
    if target is None:
        console.print("[bold red]Error:[/bold red] No target specified")
        console.print("Usage: axe chop [TARGET]")
        console.print("       axe chop .               (current directory)")
        console.print("       axe chop path            (configured path)")
        console.print("       axe chop <file/dir>      (specific path)")
        sys.exit(1)
    
    # Determine input path
    if target == 'path':
        input_path = Path(config.get('input_path', Path.cwd()))
    elif target == '.':
        input_path = Path.cwd()
    else:
        input_path = Path(target).resolve()
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir).resolve()
    else:
        output_path = Path(config.get('output_path', Path.cwd() / 'axe_output'))
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize converter
    converter = ArxivConverter(stats_manager)
    
    # Show operation header
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]Input:[/bold cyan] {input_path}\n"
        f"[bold green]Output:[/bold green] {output_path}\n"
        f"[bold yellow]Format:[/bold yellow] {format}",
        title="[bold]AXE CHOP Operation[/bold]",
        border_style="cyan"
    ))
    console.print()
    
    # Process based on input type
    try:
        if input_path.is_file():
            # Single file
            converter.process_file(input_path, output_path, format)
        elif input_path.is_dir():
            # Directory
            converter.process_directory(input_path, output_path, format)
        else:
            # Check if it's an arXiv URL
            if 'arxiv.org' in str(target):
                converter.process_url(target, output_path, format)
            else:
                console.print(f"[bold red]Error:[/bold red] Path does not exist: {input_path}")
                sys.exit(1)
        
        # Show run statistics
        stats_manager.show_run_stats()
        
        # Save persistent statistics
        stats_manager.save_persistent_stats()
        
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@axe.command()
@click.option('--show', is_flag=True, help='Show persistent statistics')
@click.option('--reset', is_flag=True, help='Reset persistent statistics')
def stats(show, reset):
    """View or manage statistics"""
    
    if reset:
        confirm = click.confirm("Are you sure you want to reset all statistics?")
        if confirm:
            stats_manager.reset_persistent_stats()
            console.print("[bold green]✓[/bold green] Statistics reset successfully")
        return
    
    if show:
        stats_manager.show_persistent_stats()
    else:
        console.print("[yellow]Use --show to display statistics or --reset to reset them[/yellow]")


@axe.command()
@click.argument('command', required=False)
def help(command):
    """Show help information for commands"""
    
    if command is None:
        console.print(Panel.fit(
            "[bold cyan]AXE CLI - ArXiv Extraction Tool[/bold cyan]\n\n"
            "[bold]Commands:[/bold]\n"
            "  [cyan]axe[/cyan]                    Launch interactive menu\n"
            "  [cyan]axe chop <target>[/cyan]     Convert arXiv papers\n"
            "  [cyan]axe path[/cyan]              Manage paths\n"
            "  [cyan]axe stats[/cyan]             View statistics\n\n"
            "[bold]Examples:[/bold]\n"
            "  [yellow]axe chop .[/yellow]              Process current directory\n"
            "  [yellow]axe chop path[/yellow]          Process configured path\n"
            "  [yellow]axe chop file.pdf[/yellow]      Process single file\n"
            "  [yellow]axe path --in ~/papers[/yellow] Set input directory\n"
            "  [yellow]axe stats --show[/yellow]       Show statistics\n\n"
            "Use [cyan]axe <command> --help[/cyan] for command-specific help",
            title="[bold]AXE CLI Help[/bold]",
            border_style="blue"
        ))
    else:
        # Show help for specific command
        ctx = click.Context(axe)
        cmd = axe.get_command(ctx, command)
        if cmd:
            console.print(Panel.fit(
                cmd.get_help(ctx),
                title=f"[bold]Help: {command}[/bold]",
                border_style="blue"
            ))
        else:
            console.print(f"[bold red]Error:[/bold red] Unknown command: {command}")


def main():
    """Entry point for the CLI"""
    try:
        axe()
    except Exception as e:
        console.print(f"\n[bold red]Fatal Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()