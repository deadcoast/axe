"""
AXE CLI - ArXiv Extraction Command Line Interface
A powerful tool for downloading and converting arXiv papers
"""

__version__ = '1.0.0'
__author__ = 'AXE CLI Team'
__description__ = 'Command-line tool for extracting and converting arXiv papers'

from .axe_cli import main, axe
from .config import Config
from .converter import ArxivConverter
from .stats import StatsManager
from .interactive import InteractiveMenu

__all__ = [
    'main',
    'axe',
    'Config',
    'ArxivConverter',
    'StatsManager',
    'InteractiveMenu'
]