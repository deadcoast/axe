"""
Auto-Save and Preferences System for AXE CLI
Implements Phase 4 features: auto-save, preferences management, and user experience optimization
Following mech_god balance system: feature(a:feat) + minimal(a:miml) = balance(a:bal)
"""

import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .ui_constants import console, get_panel_style, get_text_style, get_styled_title


class AutoSaveManager:
    """Manages auto-save functionality for user preferences and data"""

    def __init__(self, save_interval: int = 30):
        """Initialize auto-save manager

        Args:
            save_interval: Auto-save interval in seconds
        """
        self.save_interval = save_interval
        self.preferences_file = Path.home() / ".axe_cli" / "preferences.json"
        self.preferences_file.parent.mkdir(parents=True, exist_ok=True)

        self.preferences = self._load_preferences()
        self.auto_save_enabled = True
        self.last_save_time = datetime.now()

        # Start auto-save thread
        self.auto_save_thread = threading.Thread(
            target=self._auto_save_loop, daemon=True
        )
        self.auto_save_thread.start()

    def _load_preferences(self) -> Dict[str, Any]:
        """Load preferences from file

        Returns:
            Dictionary of preferences
        """
        if not self.preferences_file.exists():
            return self._get_default_preferences()

        try:
            with open(self.preferences_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._get_default_preferences()

    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences

        Returns:
            Dictionary of default preferences
        """
        return {
            "ui": {
                "theme": "default",
                "show_banner": True,
                "show_progress": True,
                "show_statistics": True,
                "compact_mode": False,
            },
            "processing": {
                "default_format": "markdown",
                "auto_create_dirs": True,
                "overwrite_existing": False,
                "max_concurrent_downloads": 3,
                "download_timeout": 30,
            },
            "paths": {
                "input_path": str(Path.cwd()),
                "output_path": str(Path.cwd() / "axe_output"),
                "remember_last_paths": True,
            },
            "logging": {
                "log_level": "INFO",
                "log_to_file": True,
                "log_file_size_limit": 10485760,  # 10MB
                "log_retention_days": 30,
            },
            "performance": {
                "cache_enabled": True,
                "cache_size_limit": 100,
                "cache_ttl_hours": 24,
                "enable_profiling": False,
            },
            "auto_save": {
                "enabled": True,
                "interval_seconds": 30,
                "save_on_exit": True,
            },
        }

    def _save_preferences(self):
        """Save preferences to file"""
        try:
            with open(self.preferences_file, "w", encoding="utf-8") as f:
                json.dump(self.preferences, f, indent=2)
            self.last_save_time = datetime.now()
        except IOError as e:
            console.print(f"[red]Error saving preferences:[/red] {e}")

    def _auto_save_loop(self):
        """Auto-save loop running in background thread"""
        while self.auto_save_enabled:
            time.sleep(self.save_interval)
            if self.auto_save_enabled:
                self._save_preferences()

    def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """Get a preference value

        Args:
            category: Preference category
            key: Preference key
            default: Default value if not found

        Returns:
            Preference value
        """
        return self.preferences.get(category, {}).get(key, default)

    def set_preference(self, category: str, key: str, value: Any):
        """Set a preference value

        Args:
            category: Preference category
            key: Preference key
            value: Value to set
        """
        if category not in self.preferences:
            self.preferences[category] = {}

        self.preferences[category][key] = value

        # Immediate save for important preferences
        if category in ["ui", "processing", "paths"]:
            self._save_preferences()

    def save_preferences(self):
        """Manually save preferences"""
        self._save_preferences()

    def load_preferences(self):
        """Manually load preferences"""
        self.preferences = self._load_preferences()

    def reset_preferences(self):
        """Reset preferences to defaults"""
        self.preferences = self._get_default_preferences()
        self._save_preferences()

    def show_preferences(self):
        """Display current preferences"""
        prefs_table = Table(**{"box": "rounded", "border_style": "blue"})
        prefs_table.add_column("Category", style=get_text_style("title"), width=15)
        prefs_table.add_column("Setting", style=get_text_style("body"), width=20)
        prefs_table.add_column("Value", style=get_text_style("success"))

        for category, settings in self.preferences.items():
            for key, value in settings.items():
                prefs_table.add_row(category, key, str(value))

        console.print()
        console.print(
            Panel.fit(
                prefs_table,
                title=get_styled_title("Current Preferences", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()

    def enable_auto_save(self):
        """Enable auto-save"""
        self.auto_save_enabled = True

    def disable_auto_save(self):
        """Disable auto-save"""
        self.auto_save_enabled = False

    def set_save_interval(self, interval: int):
        """Set auto-save interval

        Args:
            interval: Interval in seconds
        """
        self.save_interval = interval
        self.set_preference("auto_save", "interval_seconds", interval)


class PreferencesManager:
    """High-level preferences management with validation and persistence"""

    def __init__(self):
        """Initialize preferences manager"""
        self.auto_save_manager = AutoSaveManager()
        self.preferences = self.auto_save_manager.preferences
        self.validation_callbacks: Dict[str, Callable] = {}

        # Setup validation callbacks
        self._setup_validation_callbacks()

    def _setup_validation_callbacks(self):
        """Setup validation callbacks for preferences"""
        self.validation_callbacks = {
            "ui.theme": self._validate_theme,
            "ui.show_banner": self._validate_boolean,
            "ui.show_progress": self._validate_boolean,
            "ui.show_statistics": self._validate_boolean,
            "ui.compact_mode": self._validate_boolean,
            "processing.default_format": self._validate_format,
            "processing.auto_create_dirs": self._validate_boolean,
            "processing.overwrite_existing": self._validate_boolean,
            "processing.max_concurrent_downloads": self._validate_positive_int,
            "processing.download_timeout": self._validate_positive_int,
            "logging.log_level": self._validate_log_level,
            "logging.log_to_file": self._validate_boolean,
            "logging.log_file_size_limit": self._validate_positive_int,
            "logging.log_retention_days": self._validate_positive_int,
            "performance.cache_enabled": self._validate_boolean,
            "performance.cache_size_limit": self._validate_positive_int,
            "performance.cache_ttl_hours": self._validate_positive_int,
            "performance.enable_profiling": self._validate_boolean,
        }

    def _validate_theme(self, value: Any) -> bool:
        """Validate theme preference"""
        valid_themes = ["default", "light", "dark", "minimal", "colorful"]
        return isinstance(value, str) and value in valid_themes

    def _validate_boolean(self, value: Any) -> bool:
        """Validate boolean preference"""
        return isinstance(value, bool)

    def _validate_format(self, value: Any) -> bool:
        """Validate format preference"""
        valid_formats = ["text", "markdown", "both"]
        return isinstance(value, str) and value in valid_formats

    def _validate_positive_int(self, value: Any) -> bool:
        """Validate positive integer preference"""
        return isinstance(value, int) and value > 0

    def _validate_log_level(self, value: Any) -> bool:
        """Validate log level preference"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        return isinstance(value, str) and value.upper() in valid_levels

    def get(self, key: str, default: Any = None) -> Any:
        """Get preference value using dot notation

        Args:
            key: Preference key in format 'category.setting'
            default: Default value if not found

        Returns:
            Preference value
        """
        try:
            category, setting = key.split(".", 1)
            return self.preferences.get(category, {}).get(setting, default)
        except ValueError:
            return default

    def set(self, key: str, value: Any) -> bool:
        """Set preference value using dot notation

        Args:
            key: Preference key in format 'category.setting'
            value: Value to set

        Returns:
            True if successful
        """
        try:
            category, setting = key.split(".", 1)

            # Validate if callback exists
            if key in self.validation_callbacks:
                if not self.validation_callbacks[key](value):
                    console.print(f"[red]Invalid value for {key}:[/red] {value}")
                    return False

            self.auto_save_manager.set_preference(category, setting, value)
            return True
        except ValueError:
            console.print(f"[red]Invalid preference key format:[/red] {key}")
            return False

    def get_ui_preferences(self) -> Dict[str, Any]:
        """Get UI preferences

        Returns:
            Dictionary of UI preferences
        """
        return self.preferences.get("ui", {})

    def get_processing_preferences(self) -> Dict[str, Any]:
        """Get processing preferences

        Returns:
            Dictionary of processing preferences
        """
        return self.preferences.get("processing", {})

    def get_path_preferences(self) -> Dict[str, Any]:
        """Get path preferences

        Returns:
            Dictionary of path preferences
        """
        return self.preferences.get("paths", {})

    def get_logging_preferences(self) -> Dict[str, Any]:
        """Get logging preferences

        Returns:
            Dictionary of logging preferences
        """
        return self.preferences.get("logging", {})

    def get_performance_preferences(self) -> Dict[str, Any]:
        """Get performance preferences

        Returns:
            Dictionary of performance preferences
        """
        return self.preferences.get("performance", {})

    def show_preference_summary(self):
        """Display preference summary"""
        summary_table = Table(**{"box": "rounded", "border_style": "blue"})
        summary_table.add_column("Category", style=get_text_style("title"), width=15)
        summary_table.add_column(
            "Settings Count", justify="center", style=get_text_style("success")
        )
        summary_table.add_column("Last Modified", style=get_text_style("body"))

        for category, settings in self.preferences.items():
            count = len(settings)
            # Get last modified time from file
            try:
                mtime = self.auto_save_manager.preferences_file.stat().st_mtime
                last_modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            except Exception:
                last_modified = "Unknown"

            summary_table.add_row(category, str(count), last_modified)

        console.print()
        console.print(
            Panel.fit(
                summary_table,
                title=get_styled_title("Preferences Summary", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()

    def export_preferences(self, file_path: Optional[Path] = None) -> Path:
        """Export preferences to file

        Args:
            file_path: Optional export file path

        Returns:
            Path to exported file
        """
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = (
                Path.home() / ".axe_cli" / f"preferences_export_{timestamp}.json"
            )

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "preferences": self.preferences,
            "version": "1.0.0",
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)

        return file_path

    def import_preferences(self, file_path: Path) -> bool:
        """Import preferences from file

        Args:
            file_path: Path to import file

        Returns:
            True if successful
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                import_data = json.load(f)

            if "preferences" in import_data:
                self.preferences = import_data["preferences"]
                self.auto_save_manager.preferences = self.preferences
                self.auto_save_manager.save_preferences()
                return True
            else:
                console.print("[red]Invalid preferences file format[/red]")
                return False
        except Exception as e:
            console.print(f"[red]Error importing preferences:[/red] {e}")
            return False


class SessionManager:
    """Manages user sessions and state persistence"""

    def __init__(self):
        """Initialize session manager"""
        self.session_file = Path.home() / ".axe_cli" / "session.json"
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.session_data = self._load_session()
        self.session_start = datetime.now()

    def _load_session(self) -> Dict[str, Any]:
        """Load session data

        Returns:
            Dictionary of session data
        """
        if not self.session_file.exists():
            return {
                "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "start_time": datetime.now().isoformat(),
                "commands_executed": [],
                "current_directory": str(Path.cwd()),
                "last_operation": None,
            }

        try:
            with open(self.session_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._get_default_session()

    def _get_default_session(self) -> Dict[str, Any]:
        """Get default session data

        Returns:
            Dictionary of default session data
        """
        return {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "commands_executed": [],
            "current_directory": str(Path.cwd()),
            "last_operation": None,
        }

    def _save_session(self):
        """Save session data"""
        try:
            with open(self.session_file, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f, indent=2)
        except IOError:
            pass

    def add_command(self, command: str, success: bool = True):
        """Add command to session history

        Args:
            command: Command executed
            success: Whether command succeeded
        """
        command_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "success": success,
        }

        self.session_data["commands_executed"].append(command_entry)
        self.session_data["last_operation"] = command_entry

        # Keep only last 100 commands
        if len(self.session_data["commands_executed"]) > 100:
            self.session_data["commands_executed"] = self.session_data[
                "commands_executed"
            ][-100:]

        self._save_session()

    def get_session_duration(self) -> timedelta:
        """Get session duration

        Returns:
            Session duration
        """
        return datetime.now() - self.session_start

    def get_command_count(self) -> int:
        """Get number of commands executed

        Returns:
            Number of commands
        """
        return len(self.session_data["commands_executed"])

    def get_success_rate(self) -> float:
        """Get success rate of commands

        Returns:
            Success rate as percentage
        """
        commands = self.session_data["commands_executed"]
        if not commands:
            return 0.0

        successful = sum(1 for cmd in commands if cmd["success"])
        return (successful / len(commands)) * 100

    def show_session_summary(self):
        """Display session summary"""
        duration = self.get_session_duration()
        command_count = self.get_command_count()
        success_rate = self.get_success_rate()

        summary_table = Table(**{"box": "rounded", "border_style": "blue"})
        summary_table.add_column("Metric", style=get_text_style("title"), width=20)
        summary_table.add_column(
            "Value", justify="right", style=get_text_style("success")
        )

        summary_table.add_row("Session ID", self.session_data["session_id"])
        summary_table.add_row("Duration", str(duration).split(".")[0])
        summary_table.add_row("Commands Executed", str(command_count))
        summary_table.add_row("Success Rate", f"{success_rate:.1f}%")
        summary_table.add_row(
            "Current Directory", self.session_data["current_directory"]
        )

        console.print()
        console.print(
            Panel.fit(
                summary_table,
                title=get_styled_title("Session Summary", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()


# Global instances for easy access
preferences_manager = PreferencesManager()
session_manager = SessionManager()


def show_preferences_features():
    """Display available preferences features"""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Preferences & Auto-Save Features[/bold cyan]\n\n"
            "✅ Auto-save preferences and settings\n"
            "✅ Comprehensive preferences management\n"
            "✅ Session state persistence\n"
            "✅ Preferences validation\n"
            "✅ Import/export functionality\n"
            "✅ Background auto-save thread\n\n"
            "[dim]Feature Weight: +5 lbs[/dim]",
            title=get_styled_title("Preferences Features", "info"),
            **get_panel_style("info"),
        )
    )
    console.print()


if __name__ == "__main__":
    # Demo preferences features
    show_preferences_features()

    # Show preferences summary
    preferences_manager.show_preference_summary()

    # Show session summary
    session_manager.show_session_summary()
