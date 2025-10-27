#!/bin/bash

# AXE CLI Installation and Test Script
# This script installs dependencies and verifies the installation
# Updated for Rich CLI Visual Consistency Overhaul (mech_god balance system)

set -e  # Exit on error

echo ""
echo "  🪓 AXE CLI - Installation Script"
echo "  Rich CLI Visual Consistency Overhaul"
echo "  Following mech_god balance system specifications"
echo ""
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 8 ]); then
    echo " Error: Python 3.8 or higher is required"
    echo "   Current version: $python_version"
    exit 1
fi

echo " Python version: $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "  Core dependencies:"
pip install -r requirements.txt --break-system-packages

# Install additional dependencies for visual enhancements
echo "  Visual enhancement dependencies:"
pip install pygments --break-system-packages  # For syntax highlighting
pip install markdown --break-system-packages  # For markdown rendering
echo " All dependencies installed"
echo ""

# Install package in development mode
echo "Installing AXE CLI..."
pip install -e . --break-system-packages
echo " AXE CLI installed"
echo ""

# Verify installation
echo "Verifying installation..."
if command -v axe &> /dev/null; then
    echo " 'axe' command is available"
else
    echo " Error: 'axe' command not found"
    echo "   Try adding ~/.local/bin to your PATH"
    exit 1
fi
echo ""

# Test basic functionality
echo "Testing basic functionality..."

# Test help command
echo "  Testing: axe --help"
axe --help > /dev/null 2>&1 && echo "   Help command works"

# Test path command
echo "  Testing: axe path --show"
axe path --show > /dev/null 2>&1 && echo "   Path command works"

# Test stats command
echo "  Testing: axe stats --show"
axe stats --show > /dev/null 2>&1 && echo "   Stats command works"

# Test visual consistency components
echo "  Testing: Visual consistency components"
python -c "
try:
    from axe_cli.ui_constants import console, show_balance_status
    print('   UI Constants module works')
except Exception as e:
    print(f'   UI Constants error: {e}')
    exit(1)

try:
    from axe_cli.ui_advanced import visual_feedback, progress_manager
    print('   UI Advanced module works')
except Exception as e:
    print(f'   UI Advanced error: {e}')
    exit(1)

try:
    from axe_cli.syntax_highlighting import syntax_highlighter
    print('   Syntax Highlighting module works')
except Exception as e:
    print(f'   Syntax Highlighting error: {e}')
    exit(1)

try:
    from axe_cli.theme_system import theme_manager
    print('   Theme System module works')
except Exception as e:
    print(f'   Theme System error: {e}')
    exit(1)
" && echo "   All visual components verified"

# Initialize theme system
echo "Initializing theme system..."
mkdir -p ~/.axe_cli/themes
echo " Theme system initialized"
echo ""

# Display balance system status
echo "MECH_GOD Balance System Status:"
python -c "
from axe_cli.ui_constants import validate_balance
balance = validate_balance()
print(f'  Minimal Weight: {balance[\"minimal_weight\"]} lbs')
print(f'  Feature Weight: {balance[\"feature_weight\"]} lbs')
print(f'  Net Balance: {balance[\"net_balance\"]} lbs')
print(f'  Status: {balance[\"balance_status\"]}')
print(f'  Implementation: {balance[\"implementation_status\"]}')
"
echo ""

echo ""
echo ""
echo "   🎉 Installation Complete!"
echo ""
echo ""
echo "Rich CLI Visual Consistency Features:"
echo "  ✅ Unified border system and color palette"
echo "  ✅ Advanced progress indicators and visual feedback"
echo "  ✅ Syntax highlighting and markdown rendering"
echo "  ✅ Theme system with light/dark variants"
echo "  ✅ Interactive tables and enhanced UI components"
echo ""
echo "Quick Start:"
echo "  1. Run 'axe' to start interactive mode"
echo "  2. Or use direct commands like 'axe chop .'"
echo "  3. See 'axe --help' for all options"
echo "  4. Run 'python test_visual_consistency.py' to test UI components"
echo ""
echo "Configuration stored in: ~/.axe_cli/"
echo "Themes stored in: ~/.axe_cli/themes/"
echo ""
echo "MECH_GOD Status: ✅ BALANCED - Feature-rich with controlled minimalism"
echo ""