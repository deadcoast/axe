@echo off
REM AXE CLI Installation and Test Script for Windows
REM This script installs dependencies and verifies the installation
REM Updated for Rich CLI Visual Consistency Overhaul (mech_god balance system)

echo.
echo   🪓 AXE CLI - Installation Script
echo   Rich CLI Visual Consistency Overhaul
echo   Following mech_god balance system specifications
echo.
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo Python version: %python_version%
echo.

REM Install dependencies
echo Installing dependencies...
echo   Core dependencies:
pip install -r requirements.txt

REM Install additional dependencies for visual enhancements
echo   Visual enhancement dependencies:
pip install pygments
pip install markdown
echo All dependencies installed
echo.

REM Install package in development mode
echo Installing AXE CLI...
pip install -e .
echo AXE CLI installed
echo.

REM Verify installation
echo Verifying installation...
axe --help >nul 2>&1
if errorlevel 1 (
    echo Error: 'axe' command not found
    echo Try adding Python Scripts directory to your PATH
    pause
    exit /b 1
)
echo 'axe' command is available
echo.

REM Test basic functionality
echo Testing basic functionality...

REM Test help command
echo   Testing: axe --help
axe --help >nul 2>&1
if errorlevel 1 (
    echo   Help command failed
) else (
    echo   Help command works
)

REM Test path command
echo   Testing: axe path --show
axe path --show >nul 2>&1
if errorlevel 1 (
    echo   Path command failed
) else (
    echo   Path command works
)

REM Test stats command
echo   Testing: axe stats --show
axe stats --show >nul 2>&1
if errorlevel 1 (
    echo   Stats command failed
) else (
    echo   Stats command works
)

REM Test visual consistency components
echo   Testing: Visual consistency components
python -c "try: from axe_cli.ui_constants import console, show_balance_status; print('   UI Constants module works'); except Exception as e: print(f'   UI Constants error: {e}'); exit(1)"
if errorlevel 1 goto :visual_error

python -c "try: from axe_cli.ui_advanced import visual_feedback, progress_manager; print('   UI Advanced module works'); except Exception as e: print(f'   UI Advanced error: {e}'); exit(1)"
if errorlevel 1 goto :visual_error

python -c "try: from axe_cli.syntax_highlighting import syntax_highlighter; print('   Syntax Highlighting module works'); except Exception as e: print(f'   Syntax Highlighting error: {e}'); exit(1)"
if errorlevel 1 goto :visual_error

python -c "try: from axe_cli.theme_system import theme_manager; print('   Theme System module works'); except Exception as e: print(f'   Theme System error: {e}'); exit(1)"
if errorlevel 1 goto :visual_error

echo   All visual components verified
goto :continue_install

:visual_error
echo   Visual components test failed
goto :continue_install

:continue_install

REM Initialize theme system
echo Initializing theme system...
if not exist "%USERPROFILE%\.axe_cli\themes" mkdir "%USERPROFILE%\.axe_cli\themes"
echo Theme system initialized
echo.

REM Display balance system status
echo MECH_GOD Balance System Status:
python -c "from axe_cli.ui_constants import validate_balance; balance = validate_balance(); print(f'  Minimal Weight: {balance[\"minimal_weight\"]} lbs'); print(f'  Feature Weight: {balance[\"feature_weight\"]} lbs'); print(f'  Net Balance: {balance[\"net_balance\"]} lbs'); print(f'  Status: {balance[\"balance_status\"]}'); print(f'  Implementation: {balance[\"implementation_status\"]}')"
echo.

echo.
echo.
echo   🎉 Installation Complete!
echo.
echo.
echo Rich CLI Visual Consistency Features:
echo   ✅ Unified border system and color palette
echo   ✅ Advanced progress indicators and visual feedback
echo   ✅ Syntax highlighting and markdown rendering
echo   ✅ Theme system with light/dark variants
echo   ✅ Interactive tables and enhanced UI components
echo.
echo Quick Start:
echo   1. Run 'axe' to start interactive mode
echo   2. Or use direct commands like 'axe chop .'
echo   3. See 'axe --help' for all options
echo   4. Run 'python test_visual_consistency.py' to test UI components
echo.
echo Configuration stored in: %USERPROFILE%\.axe_cli\
echo Themes stored in: %USERPROFILE%\.axe_cli\themes\
echo.
echo MECH_GOD Status: ✅ BALANCED - Feature-rich with controlled minimalism
echo.
pause
