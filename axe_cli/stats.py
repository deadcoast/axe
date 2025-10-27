"""
Statistics management for AXE CLI
Tracks both per-run and persistent statistics
"""

import json
from datetime import datetime
from pathlib import Path
from rich.table import Table
from rich.panel import Panel

from .ui_constants import (
    console,
    get_panel_style,
    get_text_style,
    TABLE_STYLES,
    get_styled_title,
)


class StatsManager:
    """Manages statistics for AXE CLI operations"""

    def __init__(self):
        """Initialize statistics manager"""
        self.stats_dir = Path.home() / ".axe_cli"
        self.stats_file = self.stats_dir / "stats.json"
        self.stats_dir.mkdir(parents=True, exist_ok=True)

        # Per-run statistics (reset each operation)
        self.run_stats = {
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": datetime.now().isoformat(),
        }

        # Persistent statistics (accumulated over time)
        self.persistent_stats = self._load_persistent_stats()

    def _load_persistent_stats(self) -> dict:
        """Load persistent statistics from file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_persistent_stats()
        return self._default_persistent_stats()

    def _default_persistent_stats(self) -> dict:
        """Return default persistent statistics"""
        return {
            "total_success": 0,
            "total_failed": 0,
            "total_skipped": 0,
            "total_runs": 0,
            "first_run": datetime.now().isoformat(),
            "last_run": None,
        }

    def increment_success(self):
        """Increment success counter for current run"""
        self.run_stats["success"] += 1

    def increment_failed(self):
        """Increment failed counter for current run"""
        self.run_stats["failed"] += 1

    def increment_skipped(self):
        """Increment skipped counter for current run"""
        self.run_stats["skipped"] += 1

    def save_persistent_stats(self):
        """Save persistent statistics to file"""
        # Update persistent stats with run stats
        self.persistent_stats["total_success"] += self.run_stats["success"]
        self.persistent_stats["total_failed"] += self.run_stats["failed"]
        self.persistent_stats["total_skipped"] += self.run_stats["skipped"]
        self.persistent_stats["total_runs"] += 1
        self.persistent_stats["last_run"] = datetime.now().isoformat()

        try:
            with open(self.stats_file, "w") as f:
                json.dump(self.persistent_stats, f, indent=2)
        except IOError as e:
            console.print(
                f"[bold red]Warning:[/bold red] Could not save statistics: {e}"
            )

    def reset_persistent_stats(self):
        """Reset persistent statistics to defaults"""
        self.persistent_stats = self._default_persistent_stats()
        try:
            with open(self.stats_file, "w") as f:
                json.dump(self.persistent_stats, f, indent=2)
        except IOError as e:
            console.print(
                f"[bold red]Error:[/bold red] Could not reset statistics: {e}"
            )

    def show_run_stats(self):
        """Display statistics for current run"""
        total = (
            self.run_stats["success"]
            + self.run_stats["failed"]
            + self.run_stats["skipped"]
        )

        if total == 0:
            return

        # Calculate run duration
        start_time = datetime.fromisoformat(self.run_stats["start_time"])
        duration = datetime.now() - start_time
        duration_str = f"{duration.total_seconds():.2f}s"

        # Create table with unified styling
        table = Table(**TABLE_STYLES["primary"])
        table.add_column("Metric", style=get_text_style("title"), width=20)
        table.add_column("Count", justify="right", style=get_text_style("success"))

        table.add_row("Successful", str(self.run_stats["success"]))
        table.add_row("Failed", str(self.run_stats["failed"]))
        table.add_row("Skipped", str(self.run_stats["skipped"]))
        table.add_row("Total Processed", str(total))
        table.add_row("Duration", duration_str)

        console.print()
        console.print(
            Panel.fit(
                table,
                title=get_styled_title("Run Statistics", "success"),
                **get_panel_style("success"),
            )
        )
        console.print()

    def show_persistent_stats(self):
        """Display persistent statistics"""
        total = (
            self.persistent_stats["total_success"]
            + self.persistent_stats["total_failed"]
            + self.persistent_stats["total_skipped"]
        )

        # Calculate success rate
        success_rate = 0
        if total > 0:
            success_rate = (self.persistent_stats["total_success"] / total) * 100

        # Format dates
        first_run = "Never"
        last_run = "Never"

        if self.persistent_stats["first_run"]:
            try:
                first_run_dt = datetime.fromisoformat(
                    self.persistent_stats["first_run"]
                )
                first_run = first_run_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass

        if self.persistent_stats["last_run"]:
            try:
                last_run_dt = datetime.fromisoformat(self.persistent_stats["last_run"])
                last_run = last_run_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass

        # Create table with unified styling
        table = Table(**TABLE_STYLES["primary"])
        table.add_column("Metric", style=get_text_style("title"), width=25)
        table.add_column("Value", justify="right", style=get_text_style("success"))

        table.add_row("Total Runs", str(self.persistent_stats["total_runs"]))
        table.add_row("Total Successful", str(self.persistent_stats["total_success"]))
        table.add_row("Total Failed", str(self.persistent_stats["total_failed"]))
        table.add_row("Total Skipped", str(self.persistent_stats["total_skipped"]))
        table.add_row("Total Processed", str(total))
        table.add_row("Success Rate", f"{success_rate:.1f}%")
        table.add_row("First Run", first_run)
        table.add_row("Last Run", last_run)

        console.print()
        console.print(
            Panel.fit(
                table,
                title=get_styled_title("Persistent Statistics", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()

    def get_run_stats(self) -> dict:
        """Get current run statistics

        Returns:
            Dictionary of run statistics
        """
        return self.run_stats.copy()

    def get_persistent_stats(self) -> dict:
        """Get persistent statistics

        Returns:
            Dictionary of persistent statistics
        """
        return self.persistent_stats.copy()
