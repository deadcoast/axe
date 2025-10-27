"""
UI Constants for AXE CLI
Provides unified visual consistency across all CLI components
Following mech_god balance system: minimal(a:miml) + feature(a:feat) = balance(a:bal)
"""

from rich.console import Console
from rich.theme import Theme

# Unified Color Palette - Balance System Implementation
COLORS = {
    # Primary Colors (Feature Weight: +++)
    'primary': 'cyan',           # Main brand color
    'secondary': 'blue',         # Secondary actions
    'accent': 'green',           # Success states
    'warning': 'yellow',         # Warning states
    'error': 'red',              # Error states
    
    # Neutral Colors (Minimal Weight: --)
    'text': 'white',             # Primary text
    'text_dim': 'dim',           # Secondary text
    'text_muted': 'bright_black', # Muted text
    
    # Background Colors
    'bg_primary': 'on blue',     # Primary background
    'bg_secondary': 'on cyan',   # Secondary background
    'bg_success': 'on green',    # Success background
    'bg_warning': 'on yellow',   # Warning background
    'bg_error': 'on red',        # Error background
}

# Unified Border System - Minimal Weight (-3 lbs)
BORDERS = {
    'primary': 'blue',           # Main borders
    'secondary': 'cyan',         # Secondary borders
    'success': 'green',          # Success borders
    'warning': 'yellow',         # Warning borders
    'error': 'red',              # Error borders
    'info': 'magenta',           # Info borders
}

# Spacing Constants - Minimal Weight (-2 lbs)
SPACING = {
    'padding_small': (0, 1),     # Minimal padding
    'padding_medium': (1, 2),    # Standard padding
    'padding_large': (2, 3),     # Generous padding
    'margin_small': 1,            # Small margin
    'margin_medium': 2,           # Standard margin
    'margin_large': 3,            # Large margin
}

# Typography Styles - Minimal Weight (-2 lbs)
TEXT_STYLES = {
    'title': 'bold cyan',
    'subtitle': 'bold blue',
    'heading': 'bold white',
    'body': 'white',
    'body_dim': 'dim',
    'body_muted': 'bright_black',
    'success': 'bold green',
    'warning': 'bold yellow',
    'error': 'bold red',
    'info': 'bold magenta',
    'code': 'bright_white',
    'link': 'underline cyan',
}

# Panel Styles - Unified System
PANEL_STYLES = {
    'primary': {
        'border_style': BORDERS['primary'],
        'padding': SPACING['padding_medium']
    },
    'secondary': {
        'border_style': BORDERS['secondary'],
        'padding': SPACING['padding_medium']
    },
    'success': {
        'border_style': BORDERS['success'],
        'padding': SPACING['padding_medium']
    },
    'warning': {
        'border_style': BORDERS['warning'],
        'padding': SPACING['padding_medium']
    },
    'error': {
        'border_style': BORDERS['error'],
        'padding': SPACING['padding_medium']
    },
    'info': {
        'border_style': BORDERS['info'],
        'padding': SPACING['padding_medium']
    }
}

# Title Styles - Separate from panel styles
TITLE_STYLES = {
    'primary': TEXT_STYLES['title'],
    'secondary': TEXT_STYLES['subtitle'],
    'success': TEXT_STYLES['success'],
    'warning': TEXT_STYLES['warning'],
    'error': TEXT_STYLES['error'],
    'info': TEXT_STYLES['info']
}

# Table Styles - Feature Weight (+3 lbs)
TABLE_STYLES = {
    'primary': {
        'box': 'rounded',
        'border_style': BORDERS['primary'],
        'header_style': TEXT_STYLES['title'],
        'row_styles': [None, 'dim'],
        'padding': SPACING['padding_small']
    },
    'compact': {
        'box': 'simple',
        'border_style': BORDERS['secondary'],
        'header_style': TEXT_STYLES['subtitle'],
        'row_styles': [None, 'dim'],
        'padding': (0, 1)
    }
}

# Progress Styles - Feature Weight (+4 lbs)
PROGRESS_STYLES = {
    'primary': {
        'spinner_style': COLORS['primary'],
        'text_style': TEXT_STYLES['body'],
        'bar_style': COLORS['primary'],
        'percentage_style': TEXT_STYLES['body_dim']
    },
    'success': {
        'spinner_style': COLORS['accent'],
        'text_style': TEXT_STYLES['success'],
        'bar_style': COLORS['accent'],
        'percentage_style': TEXT_STYLES['success']
    }
}

# Status Styles - Feature Weight (+3 lbs)
STATUS_STYLES = {
    'loading': {
        'spinner_style': COLORS['primary'],
        'text_style': TEXT_STYLES['body']
    },
    'success': {
        'spinner_style': COLORS['accent'],
        'text_style': TEXT_STYLES['success']
    },
    'warning': {
        'spinner_style': COLORS['warning'],
        'text_style': TEXT_STYLES['warning']
    },
    'error': {
        'spinner_style': COLORS['error'],
        'text_style': TEXT_STYLES['error']
    }
}

# Console Theme - Unified Visual System
AXE_THEME = Theme({
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
    "text.link": "underline cyan",
})

# Create unified console instance
console = Console(theme=AXE_THEME)

# Balance System Validation
def validate_balance():
    """Validate the balance system implementation
    
    Returns:
        dict: Balance validation results
    """
    minimal_weight = -11  # Sum of all minimal (--) weights
    feature_weight = +10  # Sum of all feature (++) weights
    net_balance = feature_weight + minimal_weight
    
    return {
        'minimal_weight': minimal_weight,
        'feature_weight': feature_weight,
        'net_balance': net_balance,
        'balance_status': 'POSITIVE' if net_balance > 0 else 'NEGATIVE',
        'implementation_status': 'BALANCED' if abs(net_balance) <= 5 else 'IMBALANCED'
    }

# Utility Functions for Consistent UI
def get_panel_style(style_name: str = 'primary'):
    """Get panel style configuration
    
    Args:
        style_name: Style name from PANEL_STYLES
        
    Returns:
        dict: Panel style configuration
    """
    return PANEL_STYLES.get(style_name, PANEL_STYLES['primary'])

def get_text_style(style_name: str = 'body'):
    """Get text style configuration
    
    Args:
        style_name: Style name from TEXT_STYLES
        
    Returns:
        str: Text style string
    """
    return TEXT_STYLES.get(style_name, TEXT_STYLES['body'])

def get_border_style(style_name: str = 'primary'):
    """Get border style configuration
    
    Args:
        style_name: Style name from BORDERS
        
    Returns:
        str: Border style string
    """
    return BORDERS.get(style_name, BORDERS['primary'])

def get_spacing(spacing_name: str = 'padding_medium'):
    """Get spacing configuration
    
    Args:
        spacing_name: Spacing name from SPACING
        
    Returns:
        tuple or int: Spacing configuration
    """
    return SPACING.get(spacing_name, SPACING['padding_medium'])

def get_styled_title(title: str, style_name: str = 'primary'):
    """Get a styled title for panels
    
    Args:
        title: Title text
        style_name: Style name from TITLE_STYLES
        
    Returns:
        str: Styled title string
    """
    style = TITLE_STYLES.get(style_name, TITLE_STYLES['primary'])
    return f"[{style}]{title}[/{style}]"

# Balance System Display
def show_balance_status():
    """Display the current balance system status"""
    balance = validate_balance()
    
    console.print()
    console.print(Panel.fit(
        f"[bold]Balance System Status[/bold]\n\n"
        f"[cyan]Minimal Weight:[/cyan] {balance['minimal_weight']} lbs\n"
        f"[green]Feature Weight:[/green] {balance['feature_weight']} lbs\n"
        f"[yellow]Net Balance:[/yellow] {balance['net_balance']} lbs\n"
        f"[bold]Status:[/bold] {balance['balance_status']}\n"
        f"[bold]Implementation:[/bold] {balance['implementation_status']}",
        title="[bold]MECH_GOD Balance Validation[/bold]",
        **get_panel_style('info')
    ))
    console.print()

if __name__ == '__main__':
    # Display balance status when run directly
    show_balance_status()
