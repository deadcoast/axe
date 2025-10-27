"""
Setup script for AXE CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README if it exists
readme_path = Path(__file__).parent / 'README.md'
long_description = ''
if readme_path.exists():
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='axe-cli',
    version='1.0.0',
    author='AXE CLI Team',
    description='Command-line tool for extracting and converting arXiv papers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/axe-cli',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    install_requires=[
        'arxiv>=2.0.0',
        'arxiv2text>=0.1.0',
        'click>=8.0.0',
        'rich>=13.0.0',
    ],
    entry_points={
        'console_scripts': [
            'axe=axe_cli.axe_cli:main',
        ],
    },
    keywords='arxiv papers research pdf converter cli',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/axe-cli/issues',
        'Source': 'https://github.com/yourusername/axe-cli',
    },
)