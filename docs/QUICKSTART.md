# AXE CLI - Quick Start Guide

Get up and running with AXE CLI in under 5 minutes!

## Step 1: Install

```bash
# Clone or download the repository
cd axe_cli

# Run the installation script
chmod +x install.sh
./install.sh
```

Or manually:

```bash
pip install -r requirements.txt
pip install -e .
```

## Step 2: Verify Installation

```bash
axe --help
```

You should see the help menu. If not, ensure `~/.local/bin` is in your PATH.

## Step 3: First Run - Interactive Mode

```bash
axe
```

This launches the interactive menu where you can:
1. Chop files (convert papers)
2. Configure paths
3. View statistics
4. Get help

Navigate using the number keys (1-5).

## Step 4: First Conversion

### Option A: Interactive Mode

```bash
axe
```

Then follow the prompts:
1. Choose option `1` (Chop files)
2. Choose option `4` (Process arXiv URL)
3. Enter an arXiv URL or ID, e.g., `2103.15538`
4. Choose format (markdown/text/both)
5. Confirm output directory

### Option B: Direct Command

```bash
# Download and convert a paper by ID
axe chop https://arxiv.org/abs/2103.15538

# Or just use the ID
axe chop 2103.15538

# Convert with specific format
axe chop 2103.15538 --format both
```

## Step 5: Batch Processing

### Process Current Directory

If you have PDFs in your current directory:

```bash
axe chop .
```

### Process a Specific Directory

```bash
axe chop /path/to/papers
```

### Set Default Paths

```bash
# Set input directory (where your PDFs are)
axe path --in ~/research/papers

# Set output directory (where converted files go)
axe path --out ~/research/converted

# Now you can use 'path' as a shortcut
axe chop path
```

## Common Commands

### View Current Configuration

```bash
axe path --show
```

### View Statistics

```bash
axe stats --show
```

### Get Help

```bash
axe --help              # General help
axe chop --help         # Help for chop command
axe path --help         # Help for path command
```

## Example Workflows

### Workflow 1: Single Paper Quick Convert

```bash
axe chop https://arxiv.org/abs/2103.15538 --format markdown
```

Done! Your converted file is in `./axe_output/`

### Workflow 2: Batch Convert Directory

```bash
# Set up directories
axe path --in ~/papers
axe path --out ~/converted

# Process all papers
axe chop path --format both

# Check results
axe stats --show
```

### Workflow 3: Interactive Research Session

```bash
# Start interactive mode
axe

# In the menu:
# 1. Configure paths (option 2)
#    - Set input to your papers directory
#    - Set output to your converted directory
# 
# 2. Convert papers (option 1)
#    - Choose "Process configured path"
#    - Select format
#    - Watch the progress
#
# 3. View statistics (option 3)
#    - See how many papers processed
#    - Check success rate
```

## Output Formats

### Markdown (Default)

Best for reading and editing:
- Preserves structure (headers, lists, etc.)
- Easy to view in any markdown viewer
- Can be further converted to other formats

### Text

Plain text extraction:
- Simple, clean text
- Good for text analysis
- Smaller file size

### Both

Get both formats at once:
```bash
axe chop paper.pdf --format both
```

## Tips

### 1. Rate Limiting

arXiv has rate limits. AXE CLI respects them automatically with built-in delays.

### 2. Failed Conversions

Some papers may fail to convert due to complex formatting. Check statistics to see the success rate.

### 3. Custom Output Per Run

Override the default output directory for a specific run:

```bash
axe chop . --out ~/custom/location
```

### 4. Finding Papers

The tool recognizes:
- Direct PDF files
- arXiv URLs (abs or pdf)
- arXiv IDs (with or without version)

Examples:
- `https://arxiv.org/abs/2103.15538`
- `https://arxiv.org/pdf/2103.15538.pdf`
- `2103.15538`
- `2103.15538v1`

### 5. Configuration Location

All config and stats are stored in `~/.axe_cli/`:
- `config.json` - Your settings
- `stats.json` - Operation statistics

## Troubleshooting

### Command Not Found

Add to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### Permission Errors

Ensure write permissions for output directory:
```bash
chmod +w ~/output/directory
```

### Module Not Found

Reinstall dependencies:
```bash
pip install -r requirements.txt --break-system-packages
```

## Next Steps

- Read the full README.md for advanced features
- Explore all command options with `--help`
- Check out the examples directory (if available)
- Contribute improvements on GitHub

---
