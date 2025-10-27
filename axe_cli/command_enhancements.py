"""
Command Aliases and Shortcuts System for AXE CLI
Implements Phase 4 features: command shortcuts, aliases, and enhanced user experience
Following mech_god balance system: feature(a:feat) + minimal(a:miml) = balance(a:bal)
"""

import json
import shlex
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .ui_constants import console, get_panel_style, get_text_style, get_styled_title


class CommandAliasManager:
    """Manages command aliases and shortcuts for enhanced user experience"""

    def __init__(self):
        """Initialize alias manager"""
        self.aliases_file = Path.home() / ".axe_cli" / "aliases.json"
        self.aliases_file.parent.mkdir(parents=True, exist_ok=True)
        self.aliases = self._load_aliases()

        # Built-in aliases
        self.builtin_aliases = {
            "c": "chop",
            "p": "path",
            "s": "stats",
            "h": "help",
            "q": "quit",
            "exit": "quit",
            "ls": "path --show",
            "status": "stats --show",
            "config": "path --show",
            "convert": "chop",
            "process": "chop",
            "download": "chop",
            "extract": "chop",
        }

        # Initialize with built-in aliases if no custom ones exist
        if not self.aliases:
            self.aliases = self.builtin_aliases.copy()
            self._save_aliases()

    def _load_aliases(self) -> Dict[str, str]:
        """Load aliases from file

        Returns:
            Dictionary of aliases
        """
        if not self.aliases_file.exists():
            return {}

        try:
            with open(self.aliases_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_aliases(self):
        """Save aliases to file"""
        try:
            with open(self.aliases_file, "w", encoding="utf-8") as f:
                json.dump(self.aliases, f, indent=2)
        except IOError:
            pass

    def add_alias(self, alias: str, command: str) -> bool:
        """Add a new alias

        Args:
            alias: Alias name
            command: Command to execute

        Returns:
            True if successful
        """
        if alias in self.builtin_aliases:
            console.print(f"[yellow]Warning:[/yellow] '{alias}' is a built-in alias")
            return False

        self.aliases[alias] = command
        self._save_aliases()
        return True

    def remove_alias(self, alias: str) -> bool:
        """Remove an alias

        Args:
            alias: Alias to remove

        Returns:
            True if successful
        """
        if alias in self.builtin_aliases:
            console.print(
                f"[yellow]Warning:[/yellow] '{alias}' is a built-in alias and cannot be removed"
            )
            return False

        if alias in self.aliases:
            del self.aliases[alias]
            self._save_aliases()
            return True

        return False

    def resolve_alias(self, input_command: str) -> str:
        """Resolve alias to actual command

        Args:
            input_command: Input command string

        Returns:
            Resolved command string
        """
        parts = input_command.split()
        if not parts:
            return input_command

        first_part = parts[0]

        # Check built-in aliases first
        if first_part in self.builtin_aliases:
            resolved = self.builtin_aliases[first_part]
            if resolved == "quit":
                return "quit"
            return resolved + " " + " ".join(parts[1:])

        # Check custom aliases
        if first_part in self.aliases:
            resolved = self.aliases[first_part]
            return resolved + " " + " ".join(parts[1:])

        return input_command

    def list_aliases(self) -> Dict[str, str]:
        """List all available aliases

        Returns:
            Dictionary of all aliases
        """
        all_aliases = {}
        all_aliases.update(self.builtin_aliases)
        all_aliases.update(self.aliases)
        return all_aliases

    def show_aliases(self):
        """Display aliases in a table"""
        all_aliases = self.list_aliases()

        if not all_aliases:
            console.print("[yellow]No aliases defined[/yellow]")
            return

        alias_table = Table(**{"box": "rounded", "border_style": "blue"})
        alias_table.add_column("Alias", style=get_text_style("title"), width=15)
        alias_table.add_column("Command", style=get_text_style("body"))
        alias_table.add_column(
            "Type", justify="center", style=get_text_style("success")
        )

        # Add built-in aliases first
        for alias, command in self.builtin_aliases.items():
            alias_table.add_row(alias, command, "[blue]built-in[/blue]")

        # Add custom aliases
        for alias, command in self.aliases.items():
            if alias not in self.builtin_aliases:
                alias_table.add_row(alias, command, "[green]custom[/green]")

        console.print()
        console.print(
            Panel.fit(
                alias_table,
                title=get_styled_title("Command Aliases", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()

    def clear_custom_aliases(self):
        """Clear all custom aliases"""
        self.aliases = {}
        self._save_aliases()
        console.print("[green]Custom aliases cleared[/green]")


class CommandShortcutManager:
    """Manages keyboard shortcuts and quick commands"""

    def __init__(self):
        """Initialize shortcut manager"""
        self.shortcuts_file = Path.home() / ".axe_cli" / "shortcuts.json"
        self.shortcuts_file.parent.mkdir(parents=True, exist_ok=True)
        self.shortcuts = self._load_shortcuts()

        # Built-in shortcuts
        self.builtin_shortcuts = {
            "Ctrl+C": "interrupt",
            "Ctrl+D": "exit",
            "Ctrl+L": "clear",
            "Ctrl+R": "history",
            "Ctrl+T": "stats --show",
            "Ctrl+P": "path --show",
            "Ctrl+H": "help",
            "Ctrl+Q": "quit",
            "Tab": "complete",
            "Up": "history_up",
            "Down": "history_down",
            "Enter": "execute",
        }

        # Initialize with built-in shortcuts if no custom ones exist
        if not self.shortcuts:
            self.shortcuts = self.builtin_shortcuts.copy()
            self._save_shortcuts()

    def _load_shortcuts(self) -> Dict[str, str]:
        """Load shortcuts from file

        Returns:
            Dictionary of shortcuts
        """
        if not self.shortcuts_file.exists():
            return {}

        try:
            with open(self.shortcuts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_shortcuts(self):
        """Save shortcuts to file"""
        try:
            with open(self.shortcuts_file, "w", encoding="utf-8") as f:
                json.dump(self.shortcuts, f, indent=2)
        except IOError:
            pass

    def add_shortcut(self, key: str, action: str) -> bool:
        """Add a new shortcut

        Args:
            key: Keyboard shortcut
            action: Action to perform

        Returns:
            True if successful
        """
        if key in self.builtin_shortcuts:
            console.print(f"[yellow]Warning:[/yellow] '{key}' is a built-in shortcut")
            return False

        self.shortcuts[key] = action
        self._save_shortcuts()
        return True

    def remove_shortcut(self, key: str) -> bool:
        """Remove a shortcut

        Args:
            key: Shortcut to remove

        Returns:
            True if successful
        """
        if key in self.builtin_shortcuts:
            console.print(
                f"[yellow]Warning:[/yellow] '{key}' is a built-in shortcut and cannot be removed"
            )
            return False

        if key in self.shortcuts:
            del self.shortcuts[key]
            self._save_shortcuts()
            return True

        return False

    def get_shortcut_action(self, key: str) -> Optional[str]:
        """Get action for a shortcut

        Args:
            key: Keyboard shortcut

        Returns:
            Action string or None
        """
        return self.shortcuts.get(key)

    def show_shortcuts(self):
        """Display shortcuts in a table"""
        all_shortcuts = {}
        all_shortcuts.update(self.builtin_shortcuts)
        all_shortcuts.update(self.shortcuts)

        if not all_shortcuts:
            console.print("[yellow]No shortcuts defined[/yellow]")
            return

        shortcut_table = Table(**{"box": "rounded", "border_style": "blue"})
        shortcut_table.add_column("Shortcut", style=get_text_style("title"), width=15)
        shortcut_table.add_column("Action", style=get_text_style("body"))
        shortcut_table.add_column(
            "Type", justify="center", style=get_text_style("success")
        )

        # Add built-in shortcuts first
        for key, action in self.builtin_shortcuts.items():
            shortcut_table.add_row(key, action, "[blue]built-in[/blue]")

        # Add custom shortcuts
        for key, action in self.shortcuts.items():
            if key not in self.builtin_shortcuts:
                shortcut_table.add_row(key, action, "[green]custom[/green]")

        console.print()
        console.print(
            Panel.fit(
                shortcut_table,
                title=get_styled_title("Keyboard Shortcuts", "info"),
                **get_panel_style("info"),
            )
        )
        console.print()

    def clear_custom_shortcuts(self):
        """Clear all custom shortcuts"""
        self.shortcuts = {}
        self._save_shortcuts()
        console.print("[green]Custom shortcuts cleared[/green]")


class CommandCompletionManager:
    """Manages command completion and suggestions"""

    def __init__(self):
        """Initialize completion manager"""
        self.commands = ["chop", "path", "stats", "help", "quit", "exit"]

        self.options = {
            "chop": ["--format", "--out", "--help"],
            "path": ["--in", "--out", "--show", "--help"],
            "stats": ["--show", "--reset", "--help"],
            "help": ["--help"],
        }

        self.file_extensions = [".pdf", ".txt", ".md"]

    def get_completions(self, text: str, position: int) -> List[str]:
        """Get command completions

        Args:
            text: Current input text
            position: Cursor position

        Returns:
            List of completion suggestions
        """
        if not text.strip():
            return self.commands

        parts = text.split()
        if not parts:
            return self.commands

        # Complete command names
        if len(parts) == 1:
            return [cmd for cmd in self.commands if cmd.startswith(parts[0])]

        # Complete options
        command = parts[0]
        if command in self.options:
            current_option = parts[-1] if parts else ""
            return [
                opt for opt in self.options[command] if opt.startswith(current_option)
            ]

        return []

    def get_file_completions(self, path: str) -> List[str]:
        """Get file completions

        Args:
            path: Partial file path

        Returns:
            List of file suggestions
        """
        try:
            path_obj = Path(path)
            if path_obj.exists() and path_obj.is_dir():
                files = []
                for ext in self.file_extensions:
                    files.extend(path_obj.glob(f"*{ext}"))
                return [str(f) for f in files]
        except Exception:
            pass

        return []


class ConfigurationValidator:
    """Validates configuration with helpful error messages"""

    def __init__(self):
        """Initialize configuration validator"""
        self.config_file = Path.home() / ".axe_cli" / "config.json"
        self.validation_rules = {
            "input_path": {
                "required": False,
                "type": str,
                "validator": self._validate_path,
                "error_message": "Input path must be a valid directory",
            },
            "output_path": {
                "required": False,
                "type": str,
                "validator": self._validate_output_path,
                "error_message": "Output path must be writable",
            },
            "default_format": {
                "required": False,
                "type": str,
                "validator": self._validate_format,
                "error_message": "Default format must be one of: text, markdown, both",
            },
            "theme": {
                "required": False,
                "type": str,
                "validator": self._validate_theme,
                "error_message": "Theme must be a valid theme name",
            },
        }

    def _validate_path(self, path: str) -> bool:
        """Validate input path

        Args:
            path: Path to validate

        Returns:
            True if valid
        """
        try:
            path_obj = Path(path)
            return path_obj.exists() and path_obj.is_dir()
        except Exception:
            return False

    def _validate_output_path(self, path: str) -> bool:
        """Validate output path

        Args:
            path: Path to validate

        Returns:
            True if valid
        """
        try:
            path_obj = Path(path)
            path_obj.mkdir(parents=True, exist_ok=True)
            return path_obj.is_dir()
        except Exception:
            return False

    def _validate_format(self, format: str) -> bool:
        """Validate format

        Args:
            format: Format to validate

        Returns:
            True if valid
        """
        return format in ["text", "markdown", "both"]

    def _validate_theme(self, theme: str) -> bool:
        """Validate theme

        Args:
            theme: Theme to validate

        Returns:
            True if valid
        """
        valid_themes = ["default", "light", "dark", "minimal", "colorful"]
        return theme in valid_themes

    def validate_config(self, config: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate configuration

        Args:
            config: Configuration dictionary

        Returns:
            Dictionary of validation errors
        """
        errors = {}

        for key, value in config.items():
            if key not in self.validation_rules:
                continue

            rule = self.validation_rules[key]

            # Check type
            if not isinstance(value, rule["type"]):
                errors[key] = [
                    f"Expected {rule['type'].__name__}, got {type(value).__name__}"
                ]
                continue

            # Check validator
            if rule["validator"] and not rule["validator"](value):
                errors[key] = [rule["error_message"]]

        return errors

    def show_validation_errors(self, errors: Dict[str, List[str]]):
        """Display validation errors

        Args:
            errors: Dictionary of validation errors
        """
        if not errors:
            console.print("[green]Configuration is valid[/green]")
            return

        error_table = Table(**{"box": "rounded", "border_style": "red"})
        error_table.add_column("Setting", style=get_text_style("title"), width=20)
        error_table.add_column("Error", style=get_text_style("error"))

        for setting, error_list in errors.items():
            error_table.add_row(setting, "; ".join(error_list))

        console.print()
        console.print(
            Panel.fit(
                error_table,
                title=get_styled_title("Configuration Validation Errors", "error"),
                **get_panel_style("error"),
            )
        )
        console.print()


# Global instances for easy access
alias_manager = CommandAliasManager()
shortcut_manager = CommandShortcutManager()
completion_manager = CommandCompletionManager()
config_validator = ConfigurationValidator()


def show_command_features():
    """Display available command features"""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Command Enhancement Features[/bold cyan]\n\n"
            "✅ Command aliases and shortcuts\n"
            "✅ Keyboard shortcuts management\n"
            "✅ Command completion and suggestions\n"
            "✅ Configuration validation\n"
            "✅ Enhanced user experience\n\n"
            "[dim]Feature Weight: +5 lbs[/dim]",
            title=get_styled_title("Command Features", "info"),
            **get_panel_style("info"),
        )
    )
    console.print()


if __name__ == "__main__":
    # Demo command features
    show_command_features()

    # Show aliases
    alias_manager.show_aliases()

    # Show shortcuts
    shortcut_manager.show_shortcuts()
