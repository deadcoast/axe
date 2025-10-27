"""
Advanced Console Features for AXE CLI
Implements Phase 4 features: advanced console logging, recording, and export capabilities
Following mech_god balance system: feature(a:feat) + minimal(a:miml) = balance(a:bal)
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .ui_constants import console, get_panel_style, get_text_style, get_styled_title


class AdvancedConsoleManager:
    """Advanced console management with logging, recording, and export capabilities"""

    def __init__(self):
        """Initialize advanced console manager"""
        self.log_dir = Path.home() / ".axe_cli" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Console recording
        self.recording = False
        self.recorded_output: List[str] = []
        self.session_start = datetime.now()

        # Logging setup
        self.logger = self._setup_logger()

        # Performance tracking
        self.performance_metrics = {
            "commands_executed": 0,
            "total_execution_time": 0.0,
            "average_response_time": 0.0,
            "memory_usage": 0,
            "error_count": 0,
        }

    def _setup_logger(self) -> logging.Logger:
        """Setup structured logging with Rich handler

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger("axe_cli")
        logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Rich handler for console output
        rich_handler = RichHandler(
            console=console, show_time=True, show_path=False, markup=True
        )
        rich_handler.setLevel(logging.INFO)

        # File handler for persistent logging
        log_file = self.log_dir / f"axe_cli_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(rich_handler)
        logger.addHandler(file_handler)

        return logger

    def start_recording(self):
        """Start console output recording"""
        self.recording = True
        self.recorded_output = []
        self.session_start = datetime.now()
        self.logger.info("Console recording started")

    def stop_recording(self):
        """Stop console output recording"""
        self.recording = False
        self.logger.info("Console recording stopped")

    def record_output(self, output: str):
        """Record console output

        Args:
            output: Output string to record
        """
        if self.recording:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.recorded_output.append(f"[{timestamp}] {output}")

    def export_session(self, format: str = "json") -> Optional[str]:
        """Export recorded session

        Args:
            format: Export format (json, text, markdown)

        Returns:
            Exported content or None if no recording
        """
        if not self.recorded_output:
            return None

        session_data = {
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "duration": str(datetime.now() - self.session_start),
            "output_count": len(self.recorded_output),
            "performance_metrics": self.performance_metrics,
            "recorded_output": self.recorded_output,
        }

        if format == "json":
            return json.dumps(session_data, indent=2)
        elif format == "text":
            return self._export_as_text(session_data)
        elif format == "markdown":
            return self._export_as_markdown(session_data)

        return None

    def _export_as_text(self, session_data: Dict[str, Any]) -> str:
        """Export session as plain text

        Args:
            session_data: Session data dictionary

        Returns:
            Formatted text content
        """
        content = f"""AXE CLI Session Export
====================

Session Start: {session_data['session_start']}
Session End: {session_data['session_end']}
Duration: {session_data['duration']}
Output Count: {session_data['output_count']}

Performance Metrics:
- Commands Executed: {session_data['performance_metrics']['commands_executed']}
- Total Execution Time: {session_data['performance_metrics']['total_execution_time']:.2f}s
- Average Response Time: {session_data['performance_metrics']['average_response_time']:.2f}s
- Error Count: {session_data['performance_metrics']['error_count']}

Recorded Output:
{chr(10).join(session_data['recorded_output'])}
"""
        return content

    def _export_as_markdown(self, session_data: Dict[str, Any]) -> str:
        """Export session as markdown

        Args:
            session_data: Session data dictionary

        Returns:
            Formatted markdown content
        """
        content = f"""# AXE CLI Session Export

## Session Information
- **Start Time**: {session_data['session_start']}
- **End Time**: {session_data['session_end']}
- **Duration**: {session_data['duration']}
- **Output Count**: {session_data['output_count']}

## Performance Metrics
| Metric | Value |
|--------|-------|
| Commands Executed | {session_data['performance_metrics']['commands_executed']} |
| Total Execution Time | {session_data['performance_metrics']['total_execution_time']:.2f}s |
| Average Response Time | {session_data['performance_metrics']['average_response_time']:.2f}s |
| Error Count | {session_data['performance_metrics']['error_count']} |

## Recorded Output
```
{chr(10).join(session_data['recorded_output'])}
```
"""
        return content

    def log_command(self, command: str, execution_time: float, success: bool = True):
        """Log command execution

        Args:
            command: Command that was executed
            execution_time: Time taken to execute
            success: Whether command succeeded
        """
        self.performance_metrics["commands_executed"] += 1
        self.performance_metrics["total_execution_time"] += execution_time
        self.performance_metrics["average_response_time"] = (
            self.performance_metrics["total_execution_time"]
            / self.performance_metrics["commands_executed"]
        )

        if not success:
            self.performance_metrics["error_count"] += 1

        level = logging.INFO if success else logging.ERROR
        self.logger.log(
            level,
            f"Command '{command}' executed in {execution_time:.2f}s - {'SUCCESS' if success else 'FAILED'}",
        )

    def show_performance_stats(self):
        """Display performance statistics"""
        stats_table = Table(**{"box": "rounded", "border_style": "blue"})
        stats_table.add_column("Metric", style=get_text_style("title"), width=25)
        stats_table.add_column(
            "Value", justify="right", style=get_text_style("success")
        )

        stats_table.add_row(
            "Commands Executed", str(self.performance_metrics["commands_executed"])
        )
        stats_table.add_row(
            "Total Execution Time",
            f"{self.performance_metrics['total_execution_time']:.2f}s",
        )
        stats_table.add_row(
            "Average Response Time",
            f"{self.performance_metrics['average_response_time']:.2f}s",
        )
        stats_table.add_row("Error Count", str(self.performance_metrics["error_count"]))
        stats_table.add_row(
            "Session Duration", str(datetime.now() - self.session_start)
        )

        console.print()
        console.print(
            Panel.fit(
                stats_table,
                title=get_styled_title("Performance Statistics", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()

    def get_log_files(self) -> List[Path]:
        """Get list of available log files

        Returns:
            List of log file paths
        """
        return list(self.log_dir.glob("*.log"))

    def clear_logs(self):
        """Clear all log files"""
        for log_file in self.get_log_files():
            log_file.unlink()
        self.logger.info("All log files cleared")

    def show_log_summary(self):
        """Display log file summary"""
        log_files = self.get_log_files()

        if not log_files:
            console.print("[yellow]No log files found[/yellow]")
            return

        log_table = Table(**{"box": "rounded", "border_style": "blue"})
        log_table.add_column("Log File", style=get_text_style("title"))
        log_table.add_column("Size", justify="right", style=get_text_style("body"))
        log_table.add_column("Modified", style=get_text_style("body"))

        for log_file in sorted(
            log_files, key=lambda x: x.stat().st_mtime, reverse=True
        ):
            size = log_file.stat().st_size
            modified = datetime.fromtimestamp(log_file.stat().st_mtime)

            log_table.add_row(
                log_file.name, f"{size:,} bytes", modified.strftime("%Y-%m-%d %H:%M")
            )

        console.print()
        console.print(
            Panel.fit(
                log_table,
                title=get_styled_title("Log Files Summary", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()


class ClipboardManager:
    """Clipboard integration for copying outputs"""

    def __init__(self):
        """Initialize clipboard manager"""
        self.available = self._check_clipboard_availability()

    def _check_clipboard_availability(self) -> bool:
        """Check if clipboard functionality is available

        Returns:
            True if clipboard is available
        """
        try:
            import pyperclip

            return True
        except ImportError:
            return False

    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard

        Args:
            text: Text to copy

        Returns:
            True if successful
        """
        if not self.available:
            return False

        try:
            import pyperclip

            pyperclip.copy(text)
            return True
        except Exception:
            return False

    def get_clipboard_content(self) -> Optional[str]:
        """Get content from clipboard

        Returns:
            Clipboard content or None
        """
        if not self.available:
            return None

        try:
            import pyperclip

            return pyperclip.paste()
        except Exception:
            return None


class OutputHistoryManager:
    """Manages output history for commands and operations"""

    def __init__(self):
        """Initialize output history manager"""
        self.history_file = Path.home() / ".axe_cli" / "output_history.json"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history = self._load_history()
        self.max_history_size = 1000

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from file

        Returns:
            List of history entries
        """
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            pass

    def add_entry(self, command: str, output: str, success: bool = True):
        """Add entry to history

        Args:
            command: Command that was executed
            output: Output from command
            success: Whether command succeeded
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "output": output,
            "success": success,
        }

        self.history.append(entry)

        # Limit history size
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size :]

        self._save_history()

    def get_recent_entries(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent history entries

        Args:
            count: Number of entries to return

        Returns:
            List of recent entries
        """
        return self.history[-count:] if self.history else []

    def search_history(self, query: str) -> List[Dict[str, Any]]:
        """Search history for entries containing query

        Args:
            query: Search query

        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        return [
            entry
            for entry in self.history
            if query_lower in entry["command"].lower()
            or query_lower in entry["output"].lower()
        ]

    def clear_history(self):
        """Clear all history"""
        self.history = []
        self._save_history()

    def show_history(self, count: int = 20):
        """Display history in a table

        Args:
            count: Number of entries to display
        """
        recent_entries = self.get_recent_entries(count)

        if not recent_entries:
            console.print("[yellow]No history entries found[/yellow]")
            return

        history_table = Table(**{"box": "rounded", "border_style": "blue"})
        history_table.add_column("Time", style=get_text_style("body"), width=12)
        history_table.add_column("Command", style=get_text_style("title"), width=20)
        history_table.add_column(
            "Status", justify="center", style=get_text_style("success")
        )
        history_table.add_column("Output Preview", style=get_text_style("body"))

        for entry in reversed(recent_entries):
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M:%S")
            status = "✓" if entry["success"] else "✗"
            status_style = "green" if entry["success"] else "red"
            output_preview = (
                entry["output"][:50] + "..."
                if len(entry["output"]) > 50
                else entry["output"]
            )

            history_table.add_row(
                timestamp,
                entry["command"],
                f"[{status_style}]{status}[/{status_style}]",
                output_preview,
            )

        console.print()
        console.print(
            Panel.fit(
                history_table,
                title=get_styled_title(
                    f"Output History (Last {len(recent_entries)} entries)", "info"
                ),
                **get_panel_style("info"),
            )
        )
        console.print()


# Global instances for easy access
console_manager = AdvancedConsoleManager()
clipboard_manager = ClipboardManager()
history_manager = OutputHistoryManager()


def show_console_features():
    """Display available console features"""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Advanced Console Features[/bold cyan]\n\n"
            "✅ Structured logging with Rich handler\n"
            "✅ Console output recording and export\n"
            "✅ Performance monitoring and metrics\n"
            "✅ Output history tracking\n"
            "✅ Clipboard integration\n"
            "✅ Session management\n\n"
            "[dim]Feature Weight: +5 lbs[/dim]",
            title=get_styled_title("Console Features", "info"),
            **get_panel_style("info"),
        )
    )
    console.print()


if __name__ == "__main__":
    # Demo advanced console features
    show_console_features()

    # Test logging
    console_manager.logger.info("Advanced console features loaded successfully!")

    # Show performance stats
    console_manager.show_performance_stats()
