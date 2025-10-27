"""
Advanced UI Components for AXE CLI
Implements Phase 2 features: visual feedback, enhanced progress, and interactive elements
Following mech_god balance system: feature(a:feat) + minimal(a:miml) = balance(a:bal)
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.status import Status
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.live import Live
from rich.layout import Layout
import time
from typing import Optional, Dict, Any

from .ui_constants import console, PROGRESS_STYLES, STATUS_STYLES, get_panel_style, get_text_style, TABLE_STYLES


class VisualFeedbackSystem:
    """Enhanced visual feedback system with animations and status indicators"""
    
    def __init__(self):
        """Initialize visual feedback system"""
        self.active_statuses: Dict[str, Status] = {}
        self.active_progress: Dict[str, Progress] = {}
    
    def show_loading_status(self, message: str, status_id: str = "default", 
                          spinner_style: str = "cyan") -> Status:
        """Show a loading status with spinner
        
        Args:
            message: Status message to display
            status_id: Unique identifier for this status
            spinner_style: Style for the spinner
            
        Returns:
            Status object for manual control
        """
        status = console.status(
            message, 
            spinner_style=spinner_style,
            spinner="dots"
        )
        status.start()
        self.active_statuses[status_id] = status
        return status
    
    def update_loading_status(self, status_id: str, message: str):
        """Update an existing loading status
        
        Args:
            status_id: Status identifier
            message: New message to display
        """
        if status_id in self.active_statuses:
            self.active_statuses[status_id].update(message)
    
    def stop_loading_status(self, status_id: str):
        """Stop a loading status
        
        Args:
            status_id: Status identifier
        """
        if status_id in self.active_statuses:
            self.active_statuses[status_id].stop()
            del self.active_statuses[status_id]
    
    def show_success_message(self, message: str, details: Optional[str] = None):
        """Show a success message with visual feedback
        
        Args:
            message: Success message
            details: Optional additional details
        """
        content = f"[bold green]✓[/bold green] {message}"
        if details:
            content += f"\n[dim]{details}[/dim]"
        
        console.print(Panel.fit(
            content,
            title="[bold green]Success[/bold green]",
            **get_panel_style('success')
        ))
    
    def show_error_message(self, message: str, details: Optional[str] = None):
        """Show an error message with visual feedback
        
        Args:
            message: Error message
            details: Optional additional details
        """
        content = f"[bold red]✗[/bold red] {message}"
        if details:
            content += f"\n[dim]{details}[/dim]"
        
        console.print(Panel.fit(
            content,
            title="[bold red]Error[/bold red]",
            **get_panel_style('error')
        ))
    
    def show_warning_message(self, message: str, details: Optional[str] = None):
        """Show a warning message with visual feedback
        
        Args:
            message: Warning message
            details: Optional additional details
        """
        content = f"[bold yellow]⚠[/bold yellow] {message}"
        if details:
            content += f"\n[dim]{details}[/dim]"
        
        console.print(Panel.fit(
            content,
            title="[bold yellow]Warning[/bold yellow]",
            **get_panel_style('warning')
        ))
    
    def show_info_message(self, message: str, details: Optional[str] = None):
        """Show an info message with visual feedback
        
        Args:
            message: Info message
            details: Optional additional details
        """
        content = f"[bold cyan]ℹ[/bold cyan] {message}"
        if details:
            content += f"\n[dim]{details}[/dim]"
        
        console.print(Panel.fit(
            content,
            title="[bold cyan]Information[/bold cyan]",
            **get_panel_style('info')
        ))


class AdvancedProgressManager:
    """Enhanced progress management with multiple progress types"""
    
    def __init__(self):
        """Initialize progress manager"""
        self.active_progress: Dict[str, Progress] = {}
        self.active_tasks: Dict[str, Any] = {}
    
    def create_file_progress(self, total_files: int, progress_id: str = "files") -> Progress:
        """Create a progress bar for file processing
        
        Args:
            total_files: Total number of files to process
            progress_id: Unique identifier for this progress
            
        Returns:
            Progress object
        """
        progress = Progress(
            SpinnerColumn(style=PROGRESS_STYLES['primary']['spinner_style']),
            TextColumn("[progress.description]{task.description}", 
                      style=PROGRESS_STYLES['primary']['text_style']),
            BarColumn(style=PROGRESS_STYLES['primary']['bar_style']),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", 
                      style=PROGRESS_STYLES['primary']['percentage_style']),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        )
        
        task = progress.add_task(
            "[cyan]Processing files...", 
            total=total_files
        )
        
        self.active_progress[progress_id] = progress
        self.active_tasks[progress_id] = task
        
        return progress
    
    def create_download_progress(self, progress_id: str = "download") -> Progress:
        """Create a progress bar for downloads
        
        Args:
            progress_id: Unique identifier for this progress
            
        Returns:
            Progress object
        """
        progress = Progress(
            SpinnerColumn(style=PROGRESS_STYLES['success']['spinner_style']),
            TextColumn("[progress.description]{task.description}", 
                      style=PROGRESS_STYLES['success']['text_style']),
            BarColumn(style=PROGRESS_STYLES['success']['bar_style']),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", 
                      style=PROGRESS_STYLES['success']['percentage_style']),
            TimeElapsedColumn(),
            console=console,
            expand=True
        )
        
        task = progress.add_task(
            "[green]Downloading...", 
            total=100
        )
        
        self.active_progress[progress_id] = progress
        self.active_tasks[progress_id] = task
        
        return progress
    
    def update_progress(self, progress_id: str, description: str = None, 
                       advance: int = 1, completed: int = None):
        """Update progress for a specific task
        
        Args:
            progress_id: Progress identifier
            description: New description
            advance: Amount to advance progress
            completed: Set completed amount
        """
        if progress_id in self.active_progress and progress_id in self.active_tasks:
            task_id = self.active_tasks[progress_id]
            
            if description:
                self.active_progress[progress_id].update(task_id, description=description)
            
            if completed is not None:
                self.active_progress[progress_id].update(task_id, completed=completed)
            else:
                self.active_progress[progress_id].advance(task_id, advance)
    
    def finish_progress(self, progress_id: str):
        """Finish and clean up progress
        
        Args:
            progress_id: Progress identifier
        """
        if progress_id in self.active_progress:
            if progress_id in self.active_tasks:
                task_id = self.active_tasks[progress_id]
                self.active_progress[progress_id].update(task_id, completed=100)
            
            del self.active_progress[progress_id]
            if progress_id in self.active_tasks:
                del self.active_tasks[progress_id]


class InteractiveTable:
    """Enhanced interactive table with sorting and filtering capabilities"""
    
    def __init__(self, title: str = "", style: str = "primary"):
        """Initialize interactive table
        
        Args:
            title: Table title
            style: Table style from TABLE_STYLES
        """
        self.title = title
        self.style = style
        self.table = Table(**TABLE_STYLES.get(style, TABLE_STYLES['primary']))
        self.columns = []
        self.rows = []
        self.sort_column = None
        self.sort_reverse = False
    
    def add_column(self, header: str, style: str = None, **kwargs):
        """Add a column to the table
        
        Args:
            header: Column header
            style: Column style
            **kwargs: Additional column arguments
        """
        if style is None:
            style = get_text_style('body')
        
        self.table.add_column(header, style=style, **kwargs)
        self.columns.append(header)
    
    def add_row(self, *values):
        """Add a row to the table
        
        Args:
            *values: Row values
        """
        self.table.add_row(*values)
        self.rows.append(values)
    
    def sort_by_column(self, column_index: int, reverse: bool = False):
        """Sort table by column
        
        Args:
            column_index: Index of column to sort by
            reverse: Sort in reverse order
        """
        if 0 <= column_index < len(self.columns):
            self.rows.sort(key=lambda row: row[column_index], reverse=reverse)
            self.sort_column = column_index
            self.sort_reverse = reverse
            
            # Rebuild table
            self._rebuild_table()
    
    def _rebuild_table(self):
        """Rebuild table with current data"""
        self.table = Table(**TABLE_STYLES.get(self.style, TABLE_STYLES['primary']))
        
        # Re-add columns
        for i, header in enumerate(self.columns):
            style = get_text_style('title') if i == self.sort_column else get_text_style('body')
            self.table.add_column(header, style=style)
        
        # Re-add rows
        for row in self.rows:
            self.table.add_row(*row)
    
    def display(self):
        """Display the table in a panel"""
        console.print()
        console.print(Panel.fit(
            self.table,
            title=f"[bold]{self.title}[/bold]",
            **get_panel_style('primary')
        ))
        console.print()


class LayoutManager:
    """Advanced layout management for complex UI arrangements"""
    
    def __init__(self):
        """Initialize layout manager"""
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
    
    def create_header(self, title: str, subtitle: str = ""):
        """Create a header layout
        
        Args:
            title: Main title
            subtitle: Optional subtitle
        """
        header_content = Text()
        header_content.append(title, style=get_text_style('title'))
        if subtitle:
            header_content.append(f"\n{subtitle}", style=get_text_style('body_dim'))
        
        self.layout["header"].update(
            Panel.fit(
                header_content,
                **get_panel_style('secondary')
            )
        )
    
    def create_footer(self, message: str):
        """Create a footer layout
        
        Args:
            message: Footer message
        """
        self.layout["footer"].update(
            Panel.fit(
                message,
                **get_panel_style('info')
            )
        )
    
    def update_main(self, content):
        """Update main content area
        
        Args:
            content: Content to display in main area
        """
        self.layout["main"].update(content)
    
    def display(self):
        """Display the complete layout"""
        console.print(self.layout)


# Global instances for easy access
visual_feedback = VisualFeedbackSystem()
progress_manager = AdvancedProgressManager()
layout_manager = LayoutManager()


def show_balance_status():
    """Display the current balance system status with enhanced visuals"""
    from .ui_constants import validate_balance
    
    balance = validate_balance()
    
    # Create balance table
    balance_table = Table(**TABLE_STYLES['primary'])
    balance_table.add_column("Metric", style=get_text_style('title'), width=20)
    balance_table.add_column("Value", justify="right", style=get_text_style('success'))
    
    balance_table.add_row("Minimal Weight", f"{balance['minimal_weight']} lbs")
    balance_table.add_row("Feature Weight", f"{balance['feature_weight']} lbs")
    balance_table.add_row("Net Balance", f"{balance['net_balance']} lbs")
    
    # Status color based on balance
    status_color = "green" if balance['balance_status'] == 'POSITIVE' else "red"
    balance_table.add_row("Status", f"[{status_color}]{balance['balance_status']}[/{status_color}]")
    balance_table.add_row("Implementation", f"[cyan]{balance['implementation_status']}[/cyan]")
    
    console.print()
    console.print(Panel.fit(
        balance_table,
        title="[bold]MECH_GOD Balance Validation[/bold]",
        **get_panel_style('info')
    ))
    console.print()


if __name__ == '__main__':
    # Demo the advanced UI components
    visual_feedback.show_success_message("Advanced UI components loaded successfully!")
    show_balance_status()
