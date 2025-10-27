"""
Theme System for AXE CLI
Implements Phase 3 features: theme system with light/dark variants and custom theme support
Following mech_god balance system: feature(a:feat) + minimal(a:miml) = balance(a:bal)
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel

from .ui_constants import console, get_panel_style, get_text_style


class ThemeManager:
    """Advanced theme management system"""
    
    def __init__(self):
        """Initialize theme manager"""
        self.themes_dir = Path.home() / '.axe_cli' / 'themes'
        self.themes_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_theme = 'default'
        self.available_themes = self._load_builtin_themes()
        self.custom_themes = self._load_custom_themes()
        
        # Apply default theme
        self.apply_theme('default')
    
    def _load_builtin_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load built-in themes
        
        Returns:
            Dictionary of built-in themes
        """
        return {
            'default': {
                'name': 'Default',
                'description': 'Default AXE CLI theme with cyan accents',
                'colors': {
                    'primary': 'cyan',
                    'secondary': 'blue',
                    'accent': 'green',
                    'warning': 'yellow',
                    'error': 'red',
                    'text': 'white',
                    'text_dim': 'dim',
                    'text_muted': 'bright_black',
                    'bg_primary': 'on blue',
                    'bg_secondary': 'on cyan',
                    'bg_success': 'on green',
                    'bg_warning': 'on yellow',
                    'bg_error': 'on red'
                },
                'borders': {
                    'primary': 'blue',
                    'secondary': 'cyan',
                    'success': 'green',
                    'warning': 'yellow',
                    'error': 'red',
                    'info': 'magenta'
                },
                'rich_theme': {
                    "info": "cyan",
                    "warning": "yellow",
                    "error": "red",
                    "success": "green",
                    "dim": "bright_black",
                    "text": "white",
                    "text.bold": "bold white",
                    "text.title": "bold cyan",
                    "text.subtitle": "bold blue",
                    "text.success": "bold green",
                    "text.warning": "bold yellow",
                    "text.error": "bold red",
                    "text.info": "bold magenta",
                    "text.code": "bright_white",
                    "text.link": "underline cyan"
                }
            },
            'light': {
                'name': 'Light',
                'description': 'Light theme with dark text on light backgrounds',
                'colors': {
                    'primary': 'blue',
                    'secondary': 'cyan',
                    'accent': 'green',
                    'warning': 'yellow',
                    'error': 'red',
                    'text': 'black',
                    'text_dim': 'bright_black',
                    'text_muted': 'white',
                    'bg_primary': 'on white',
                    'bg_secondary': 'on bright_white',
                    'bg_success': 'on green',
                    'bg_warning': 'on yellow',
                    'bg_error': 'on red'
                },
                'borders': {
                    'primary': 'blue',
                    'secondary': 'cyan',
                    'success': 'green',
                    'warning': 'yellow',
                    'error': 'red',
                    'info': 'magenta'
                },
                'rich_theme': {
                    "info": "blue",
                    "warning": "yellow",
                    "error": "red",
                    "success": "green",
                    "dim": "bright_black",
                    "text": "black",
                    "text.bold": "bold black",
                    "text.title": "bold blue",
                    "text.subtitle": "bold cyan",
                    "text.success": "bold green",
                    "text.warning": "bold yellow",
                    "text.error": "bold red",
                    "text.info": "bold magenta",
                    "text.code": "bright_black",
                    "text.link": "underline blue"
                }
            },
            'dark': {
                'name': 'Dark',
                'description': 'Dark theme with bright accents on dark backgrounds',
                'colors': {
                    'primary': 'bright_cyan',
                    'secondary': 'bright_blue',
                    'accent': 'bright_green',
                    'warning': 'bright_yellow',
                    'error': 'bright_red',
                    'text': 'bright_white',
                    'text_dim': 'white',
                    'text_muted': 'bright_black',
                    'bg_primary': 'on black',
                    'bg_secondary': 'on bright_black',
                    'bg_success': 'on green',
                    'bg_warning': 'on yellow',
                    'bg_error': 'on red'
                },
                'borders': {
                    'primary': 'bright_blue',
                    'secondary': 'bright_cyan',
                    'success': 'bright_green',
                    'warning': 'bright_yellow',
                    'error': 'bright_red',
                    'info': 'bright_magenta'
                },
                'rich_theme': {
                    "info": "bright_cyan",
                    "warning": "bright_yellow",
                    "error": "bright_red",
                    "success": "bright_green",
                    "dim": "white",
                    "text": "bright_white",
                    "text.bold": "bold bright_white",
                    "text.title": "bold bright_cyan",
                    "text.subtitle": "bold bright_blue",
                    "text.success": "bold bright_green",
                    "text.warning": "bold bright_yellow",
                    "text.error": "bold bright_red",
                    "text.info": "bold bright_magenta",
                    "text.code": "bright_white",
                    "text.link": "underline bright_cyan"
                }
            },
            'minimal': {
                'name': 'Minimal',
                'description': 'Minimal theme with reduced visual noise',
                'colors': {
                    'primary': 'white',
                    'secondary': 'dim',
                    'accent': 'green',
                    'warning': 'yellow',
                    'error': 'red',
                    'text': 'white',
                    'text_dim': 'dim',
                    'text_muted': 'bright_black',
                    'bg_primary': 'default',
                    'bg_secondary': 'default',
                    'bg_success': 'default',
                    'bg_warning': 'default',
                    'bg_error': 'default'
                },
                'borders': {
                    'primary': 'white',
                    'secondary': 'dim',
                    'success': 'green',
                    'warning': 'yellow',
                    'error': 'red',
                    'info': 'magenta'
                },
                'rich_theme': {
                    "info": "white",
                    "warning": "yellow",
                    "error": "red",
                    "success": "green",
                    "dim": "bright_black",
                    "text": "white",
                    "text.bold": "bold white",
                    "text.title": "bold white",
                    "text.subtitle": "bold dim",
                    "text.success": "bold green",
                    "text.warning": "bold yellow",
                    "text.error": "bold red",
                    "text.info": "bold magenta",
                    "text.code": "bright_white",
                    "text.link": "underline white"
                }
            },
            'colorful': {
                'name': 'Colorful',
                'description': 'Colorful theme with vibrant colors',
                'colors': {
                    'primary': 'magenta',
                    'secondary': 'cyan',
                    'accent': 'bright_green',
                    'warning': 'bright_yellow',
                    'error': 'bright_red',
                    'text': 'bright_white',
                    'text_dim': 'white',
                    'text_muted': 'bright_black',
                    'bg_primary': 'on magenta',
                    'bg_secondary': 'on cyan',
                    'bg_success': 'on bright_green',
                    'bg_warning': 'on bright_yellow',
                    'bg_error': 'on bright_red'
                },
                'borders': {
                    'primary': 'magenta',
                    'secondary': 'cyan',
                    'success': 'bright_green',
                    'warning': 'bright_yellow',
                    'error': 'bright_red',
                    'info': 'bright_magenta'
                },
                'rich_theme': {
                    "info": "magenta",
                    "warning": "bright_yellow",
                    "error": "bright_red",
                    "success": "bright_green",
                    "dim": "white",
                    "text": "bright_white",
                    "text.bold": "bold bright_white",
                    "text.title": "bold magenta",
                    "text.subtitle": "bold cyan",
                    "text.success": "bold bright_green",
                    "text.warning": "bold bright_yellow",
                    "text.error": "bold bright_red",
                    "text.info": "bold bright_magenta",
                    "text.code": "bright_white",
                    "text.link": "underline magenta"
                }
            }
        }
    
    def _load_custom_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load custom themes from files
        
        Returns:
            Dictionary of custom themes
        """
        custom_themes = {}
        
        for theme_file in self.themes_dir.glob('*.json'):
            try:
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                    theme_name = theme_file.stem
                    custom_themes[theme_name] = theme_data
            except (json.JSONDecodeError, IOError) as e:
                console.print(f"[bold red]Warning:[/bold red] Could not load custom theme {theme_file}: {e}")
        
        return custom_themes
    
    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme
        
        Args:
            theme_name: Name of the theme to apply
            
        Returns:
            True if theme was applied successfully
        """
        theme_data = self.get_theme(theme_name)
        
        if not theme_data:
            console.print(f"[bold red]Error:[/bold red] Theme '{theme_name}' not found")
            return False
        
        # Update global console theme
        global console
        console = Console(theme=Theme(theme_data['rich_theme']))
        
        # Update current theme
        self.current_theme = theme_name
        
        # Save theme preference
        self._save_theme_preference(theme_name)
        
        return True
    
    def get_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Get theme data
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Theme data or None if not found
        """
        # Check built-in themes first
        if theme_name in self.available_themes:
            return self.available_themes[theme_name]
        
        # Check custom themes
        if theme_name in self.custom_themes:
            return self.custom_themes[theme_name]
        
        return None
    
    def list_themes(self) -> Dict[str, str]:
        """List all available themes
        
        Returns:
            Dictionary of theme names and descriptions
        """
        themes = {}
        
        # Add built-in themes
        for name, data in self.available_themes.items():
            themes[name] = f"[built-in] {data['description']}"
        
        # Add custom themes
        for name, data in self.custom_themes.items():
            themes[name] = f"[custom] {data.get('description', 'Custom theme')}"
        
        return themes
    
    def create_custom_theme(self, name: str, base_theme: str = 'default', 
                           modifications: Optional[Dict[str, Any]] = None) -> bool:
        """Create a custom theme
        
        Args:
            name: Name for the custom theme
            base_theme: Base theme to modify
            modifications: Modifications to apply
            
        Returns:
            True if theme was created successfully
        """
        base_data = self.get_theme(base_theme)
        
        if not base_data:
            console.print(f"[bold red]Error:[/bold red] Base theme '{base_theme}' not found")
            return False
        
        # Create new theme data
        custom_theme = base_data.copy()
        custom_theme['name'] = name.title()
        custom_theme['description'] = f"Custom theme based on {base_theme}"
        
        # Apply modifications
        if modifications:
            if 'colors' in modifications:
                custom_theme['colors'].update(modifications['colors'])
            if 'borders' in modifications:
                custom_theme['borders'].update(modifications['borders'])
            if 'rich_theme' in modifications:
                custom_theme['rich_theme'].update(modifications['rich_theme'])
        
        # Save custom theme
        theme_file = self.themes_dir / f"{name}.json"
        
        try:
            with open(theme_file, 'w') as f:
                json.dump(custom_theme, f, indent=2)
            
            # Reload custom themes
            self.custom_themes = self._load_custom_themes()
            
            console.print(f"[bold green]✓[/bold green] Custom theme '{name}' created successfully")
            return True
        
        except IOError as e:
            console.print(f"[bold red]Error:[/bold red] Could not save custom theme: {e}")
            return False
    
    def delete_custom_theme(self, name: str) -> bool:
        """Delete a custom theme
        
        Args:
            name: Name of the theme to delete
            
        Returns:
            True if theme was deleted successfully
        """
        if name not in self.custom_themes:
            console.print(f"[bold red]Error:[/bold red] Custom theme '{name}' not found")
            return False
        
        theme_file = self.themes_dir / f"{name}.json"
        
        try:
            theme_file.unlink()
            del self.custom_themes[name]
            console.print(f"[bold green]✓[/bold green] Custom theme '{name}' deleted successfully")
            return True
        
        except IOError as e:
            console.print(f"[bold red]Error:[/bold red] Could not delete custom theme: {e}")
            return False
    
    def _save_theme_preference(self, theme_name: str):
        """Save theme preference to file
        
        Args:
            theme_name: Name of the theme
        """
        config_file = Path.home() / '.axe_cli' / 'theme.json'
        
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump({'current_theme': theme_name}, f, indent=2)
        except IOError:
            pass  # Ignore errors saving theme preference
    
    def _load_theme_preference(self) -> str:
        """Load theme preference from file
        
        Returns:
            Preferred theme name or 'default'
        """
        config_file = Path.home() / '.axe_cli' / 'theme.json'
        
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('current_theme', 'default')
        except (json.JSONDecodeError, IOError):
            pass
        
        return 'default'
    
    def show_theme_preview(self, theme_name: str):
        """Show a preview of a theme
        
        Args:
            theme_name: Theme to preview
        """
        theme_data = self.get_theme(theme_name)
        
        if not theme_data:
            console.print(f"[bold red]Error:[/bold red] Theme '{theme_name}' not found")
            return
        
        # Create preview content
        preview_content = f"""[bold {theme_data['colors']['primary']}]Primary Color[/bold {theme_data['colors']['primary']}]
[{theme_data['colors']['secondary']}]Secondary Color[/{theme_data['colors']['secondary']}]
[{theme_data['colors']['accent']}]Success Message[/{theme_data['colors']['accent']}]
[{theme_data['colors']['warning']}]Warning Message[/{theme_data['colors']['warning']}]
[{theme_data['colors']['error']}]Error Message[/{theme_data['colors']['error']}]

[bold]Description:[/bold] {theme_data['description']}
[bold]Type:[/bold] {'Built-in' if theme_name in self.available_themes else 'Custom'}"""
        
        console.print()
        console.print(Panel.fit(
            preview_content,
            title=f"[bold]{theme_data['name']} Theme Preview[/bold]",
            border_style=theme_data['borders']['primary']
        ))
        console.print()
    
    def show_theme_manager(self):
        """Display theme management interface"""
        themes = self.list_themes()
        
        console.print()
        console.print(Panel.fit(
            "[bold cyan]Theme Manager[/bold cyan]\n\n"
            f"[bold]Current Theme:[/bold] {self.current_theme}\n\n"
            "[bold]Available Themes:[/bold]\n" +
            "\n".join([f"  [cyan]{name}[/cyan]: {desc}" for name, desc in themes.items()]) +
            "\n\n[bold]Commands:[/bold]\n"
            "  • [yellow]apply <theme>[/yellow] - Apply a theme\n"
            "  • [yellow]preview <theme>[/yellow] - Preview a theme\n"
            "  • [yellow]create <name> <base>[/yellow] - Create custom theme\n"
            "  • [yellow]delete <name>[/yellow] - Delete custom theme",
            title="[bold]Theme Management[/bold]",
            **get_panel_style('info')
        ))
        console.print()


# Global theme manager instance
theme_manager = ThemeManager()


def show_theme_status():
    """Display current theme status"""
    console.print()
    console.print(Panel.fit(
        f"[bold]Current Theme:[/bold] [cyan]{theme_manager.current_theme}[/cyan]\n"
        f"[bold]Available Themes:[/bold] {len(theme_manager.list_themes())}\n"
        f"[bold]Custom Themes:[/bold] {len(theme_manager.custom_themes)}",
        title="[bold]Theme Status[/bold]",
        **get_panel_style('primary')
    ))
    console.print()


if __name__ == '__main__':
    # Demo theme system
    theme_manager.show_theme_manager()
    show_theme_status()
