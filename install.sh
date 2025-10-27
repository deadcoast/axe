#!/bin/bash

# AXE CLI Installation and Test Script
# This script installs dependencies and verifies the installation

set -e  # Exit on error

echo ""
echo "  🪓 AXE CLI - Installation Script"
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
pip install -r requirements.txt --break-system-packages
echo " Dependencies installed"
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

echo ""
echo ""
echo "   Installation Complete!"
echo ""
echo ""
echo "Quick Start:"
echo "  1. Run 'axe' to start interactive mode"
echo "  2. Or use direct commands like 'axe chop .'"
echo "  3. See 'axe --help' for all options"
echo ""
echo "Configuration stored in: ~/.axe_cli/"
echo ""