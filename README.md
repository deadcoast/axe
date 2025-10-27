---
title: "AXE CLI: ArXiv Extraction Tool"
description: "A command-line tool to fetch and convert arXiv papers from PDF to clean Markdown text."
author: "deadcoast"
date: "2025-10-27"
version: "0.0.1"
license: "MIT"
repository: "https://github.com/deadcoast/axe-cli"
# Use 'tags' for specific, granular topics.
tags:
  - arXiv
  - CLI
  - tool
  - conversion
  - markdown
  - text
  - pdf
# Use 'keywords' for SEO; can be more descriptive phrases.
keywords: "arXiv, CLI, tool, conversion, markdown, text, PDF"
# 'Category' is usually for broader classification. Often just one is used.
category: "Conversion Tools"
---

**🪓**

---

_Powerful, interactive command-line tool for downloading and converting arXiv papers to text and markdown formats._

## Features

- Fast Downloads: Direct arXiv API integration
- Multiple Formats: Convert to text, markdown, or both
- Beautiful CLI: Rich terminal UI with progress bars
- Batch Processing: Process entire directories at once
- Statistics Tracking: Persistent and per-run statistics
- Configurable: Save default paths and preferences
- Two Modes: Interactive menu or direct commands

## Installation

### Quick Install

```bash
uv pip install -r requirements.txt
uv pip install -e .
```

### From Source

```bash
git clone https://github.com/yourusername/axe-cli.git
cd axe-cli
uv pip install -r requirements.txt
uv pip install -e .
```

## Usage

### Interactive Mode

Simply run `axe` to launch the interactive menu:

```bash
axe
```

The interactive menu provides a user-friendly interface for all operations:
- Chop files (convert papers)
- Configure paths
- View statistics
- Help & documentation

### Direct Commands

#### Process Current Directory

```bash
axe chop .
```

#### Process Configured Path

```bash
axe chop path
```

#### Process Specific File

```bash
axe chop /path/to/paper.pdf
```

#### Process arXiv URL

```bash
axe chop https://arxiv.org/abs/2103.15538
```

#### Configure Paths

```bash
# Set input directory
axe path --in ~/research/papers

# Set output directory
axe path --out ~/research/converted

# Show current paths
axe path --show
```

#### View Statistics

```bash
# Show persistent statistics
axe stats --show

# Reset statistics
axe stats --reset
```

#### Output Format Options

```bash
# Text only
axe chop paper.pdf --format text

# Markdown only (default)
axe chop paper.pdf --format markdown

# Both formats
axe chop paper.pdf --format both
```

## Command Reference

### Root Command: `axe`

The root command. Run alone to start interactive mode, or combine with subcommands.

### Subcommands

#### `chop` - Convert Papers

Convert arXiv papers to text/markdown.

Syntax:
```bash
axe chop [TARGET] [OPTIONS]
```

Targets:
- `.` - Current directory
- `path` - Configured default path
- `/path/to/file` - Specific file path
- `/path/to/dir` - Specific directory
- `https://arxiv.org/...` - arXiv URL

Options:
- `--format, -f` - Output format: `text`, `markdown`, or `both` (default: `markdown`)
- `--out` - Override output directory for this operation

Examples:
```bash
axe chop .                           # Current directory
axe chop path                        # Configured path
axe chop paper.pdf                   # Single file
axe chop papers/                     # Directory
axe chop https://arxiv.org/abs/2103  # URL
axe chop . --format both             # Multiple formats
axe chop . --out ~/custom/output     # Custom output
```

#### `path` - Manage Paths

Configure default input and output directories.

Options:
- `--in` - Set input directory
- `--out` - Set output directory
- `--show` - Display current paths

Examples:
```bash
axe path --in ~/papers           # Set input
axe path --out ~/converted       # Set output
axe path --show                  # Show paths
axe path --in ~/papers --out ~/converted  # Set both
```

#### `stats` - View Statistics

View or manage operation statistics.

Options:
- `--show` - Display persistent statistics
- `--reset` - Reset all statistics

Examples:
```bash
axe stats --show    # View stats
axe stats --reset   # Reset stats
```

#### `help` - Get Help

Display help information.

Examples:
```bash
axe help           # General help
axe help chop      # Help for chop command
axe chop --help    # Also works
```

## Configuration

AXE CLI stores configuration in `~/.axe_cli/`:

```
~/.axe_cli/
 config.json    # Configuration settings
 stats.json     # Persistent statistics
```

### Default Configuration

```json
{
  "input_path": "/current/directory",
  "output_path": "/current/directory/axe_output",
  "default_format": "markdown"
}
```

## Statistics

AXE CLI tracks two types of statistics:

### Per-Run Statistics

Displayed after each operation:
- Successful conversions
- Failed conversions
- Skipped files
- Total processed
- Duration

### Persistent Statistics

Accumulated over time:
- Total runs
- Total successful
- Total failed
- Total skipped
- Success rate
- First run date
- Last run date

View with `axe stats --show` or through the interactive menu.

## Supported Input Formats

- PDF files - Direct PDF files from arXiv
- arXiv URLs - Both abstract and PDF URLs
  - `https://arxiv.org/abs/XXXX.XXXXX`
  - `https://arxiv.org/pdf/XXXX.XXXXX`
- arXiv IDs - Just the ID number
  - `2103.15538`
  - `2103.15538v1`

## Output Formats

### Text (.txt)

Plain text extraction from the PDF.

### Markdown (.md)

Formatted markdown with preserved structure:
- Headers
- Paragraphs
- Lists
- Equations (where possible)
- Tables

## Examples

### Basic Workflow

```bash
# 1. Set up paths
axe path --in ~/research/papers
axe path --out ~/research/converted

# 2. Process all papers
axe chop path --format markdown

# 3. Check results
axe stats --show
```

### Single Paper Workflow

```bash
# Download and convert from URL
axe chop https://arxiv.org/abs/2103.15538 --format both
```

### Interactive Workflow

```bash
# Start interactive mode
axe

# Navigate through menus:
# 1. Chop files
# 2. Process specific file
# 3. Enter file path
# 4. Choose format
# 5. View results
```

## Troubleshooting

### arxiv2text not found

```bash
pip install arxiv2text
```

### Permission errors

Ensure you have write permissions for the output directory.

### Rate limiting

If processing many papers, the tool includes delays to respect arXiv's rate limits.

### Conversion failures

Some papers may fail to convert due to:
- Complex LaTeX formatting
- Non-standard PDF structure
- Scanned images instead of text

Check the statistics to see how many succeeded/failed.

## Development

### Project Structure

```
axe_cli/
 __init__.py       # Package initialization
 axe_cli.py        # Main CLI entry point
 config.py         # Configuration management
 converter.py      # Conversion logic
 interactive.py    # Interactive menu
 stats.py          # Statistics tracking
```

### Running Tests

```bash
# Test installation
axe --help

# Test conversion
axe chop https://arxiv.org/abs/2103.15538

# Test interactive mode
axe
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful CLI
- Uses [arxiv](https://github.com/lukasschwab/arxiv.py) for arXiv API
- Uses [arxiv2text](https://pypi.org/project/arxiv2text/) for conversion
- Powered by [Click](https://click.palletsprojects.com/) for CLI framework

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Read the documentation thoroughly

---

## **🪓**
---
