# AXE CLI - Usage Examples

This file contains comprehensive examples of using AXE CLI.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Path Management](#path-management)
3. [Batch Processing](#batch-processing)
4. [Format Options](#format-options)
5. [Statistics](#statistics)
6. [Interactive Mode](#interactive-mode)
7. [Advanced Workflows](#advanced-workflows)

---

## Basic Usage

### Download and Convert Single Paper by URL

```bash
# Full URL
axe chop https://arxiv.org/abs/2103.15538

# PDF URL also works
axe chop https://arxiv.org/pdf/2103.15538.pdf
```

### Download and Convert by arXiv ID

```bash
# Basic ID
axe chop 2103.15538

# With version number
axe chop 2103.15538v1
```

### Convert Local PDF

```bash
# Single file
axe chop paper.pdf

# With full path
axe chop /home/user/papers/quantum_computing.pdf
```

---

## Path Management

### View Current Paths

```bash
axe path --show
```

Output:
```
 Path Configuration 
 Input Path: /home/user   
 Output Path: /home/user/axe_output 

```

### Set Input Directory

```bash
# Set where your papers are stored
axe path --in ~/research/papers

# Use absolute path
axe path --in /home/user/Documents/arxiv_papers
```

### Set Output Directory

```bash
# Set where converted files should go
axe path --out ~/research/converted

# Create new directory
axe path --out ~/new_output_folder
```

### Set Both at Once

```bash
axe path --in ~/papers --out ~/converted
```

---

## Batch Processing

### Process Current Directory

```bash
# Convert all PDFs in current directory
axe chop .
```

### Process Configured Path

```bash
# First set the path
axe path --in ~/papers

# Then process it
axe chop path
```

### Process Specific Directory

```bash
# Process all PDFs in a specific directory
axe chop ~/research/papers
axe chop /path/to/directory
```

### Override Output Directory

```bash
# Process with custom output location
axe chop . --out ~/custom_output
axe chop path --out /tmp/converted
```

---

## Format Options

### Text Format Only

```bash
axe chop paper.pdf --format text
axe chop 2103.15538 --format text
```

Output: `paper.txt`

### Markdown Format (Default)

```bash
axe chop paper.pdf --format markdown
# or simply
axe chop paper.pdf
```

Output: `paper.md`

### Both Formats

```bash
axe chop paper.pdf --format both
```

Output: `paper.txt` and `paper.md`

### Batch with Format

```bash
# Convert all papers in directory to both formats
axe chop ~/papers --format both

# Current directory, text only
axe chop . --format text
```

---

## Statistics

### View Statistics

```bash
axe stats --show
```

Output:
```
             Persistent Statistics              

 Metric                            Value 

 Total Runs                           15 
 Total Successful                     47 
 Total Failed                          3 
 Total Skipped                         2 
 Total Processed                      52 
 Success Rate                      90.4% 
 First Run                 2025-01-15 10:30 
 Last Run                  2025-01-20 14:22 

```

### Reset Statistics

```bash
axe stats --reset
```

Note: This will prompt for confirmation.

---

## Interactive Mode

### Launch Interactive Menu

```bash
axe
```

Menu Display:
```

   🪓 AXE CLI                        
   ArXiv Extraction Tool             
   Interactive Mode                  


 Main Menu 
  1  Chop files (convert     
     arXiv papers)           
                             
  2  Configure paths         
                             
  3  View statistics         
                             
  4  Help & Documentation    
                             
  5  Exit                    


Choose an option [1]:
```

### Interactive Chop Operation

1. Choose `1` (Chop files)
2. Select operation type:
   - `1` Process current directory
   - `2` Process configured path
   - `3` Process specific file/directory
   - `4` Process arXiv URL
3. Choose output format
4. Confirm or set output directory
5. Watch progress and results

### Interactive Path Configuration

1. Choose `2` (Configure paths)
2. Select operation:
   - `1` Set input path
   - `2` Set output path
   - `3` View current paths
   - `4` Reset to defaults

### Interactive Statistics

1. Choose `3` (View statistics)
2. Select operation:
   - `1` View persistent statistics
   - `2` Reset statistics

---

## Advanced Workflows

### Research Paper Collection Workflow

```bash
# 1. Set up your workspace
axe path --in ~/research/papers/2025
axe path --out ~/research/converted/2025

# 2. Download papers by ID (manually or scripted)
# Place PDFs in ~/research/papers/2025

# 3. Batch convert everything
axe chop path --format both

# 4. Check results
axe stats --show
```

### Quick Single Paper Workflow

```bash
# One command to download and convert
axe chop 2103.15538 --format markdown --out ~/current_project
```

### Daily Paper Processing

```bash
#!/bin/bash
# daily_papers.sh - Process new papers daily

# Set date-based directory
TODAY=$(date +%Y-%m-%d)
mkdir -p ~/papers/$TODAY

# Process papers
axe chop ~/papers/$TODAY --format both --out ~/converted/$TODAY

# View stats
axe stats --show
```

### Multi-Directory Processing

```bash
# Process multiple directories
for dir in ~/papers/*/; do
    echo "Processing $dir"
    axe chop "$dir" --format markdown
done
```

### Custom Output Structure

```bash
# Organize by topic
axe chop quantum_papers/ --out ~/converted/quantum
axe chop ml_papers/ --out ~/converted/machine_learning
axe chop physics_papers/ --out ~/converted/physics
```

### Error Recovery

```bash
# If some papers fail, you can:
# 1. Check stats to see failure count
axe stats --show

# 2. Re-run on specific files
axe chop failed_paper.pdf

# 3. Try different format
axe chop failed_paper.pdf --format text
```

---

## Command Chaining Examples

### Set Path and Process

```bash
axe path --in ~/papers && axe chop path
```

### Process Multiple Specific Files

```bash
axe chop paper1.pdf && axe chop paper2.pdf && axe chop paper3.pdf
```

### Process and View Stats

```bash
axe chop . --format both && axe stats --show
```

---

## Integration Examples

### With Find Command

```bash
# Find all PDFs and convert them
find ~/papers -name "*.pdf" -exec axe chop {} \;
```

### With Cron Job

```bash
# Add to crontab (crontab -e)
# Run daily at 2 AM
0 2 * * * /usr/local/bin/axe chop ~/papers/daily --format markdown
```

### With Shell Script

```bash
#!/bin/bash
# convert_arxiv_list.sh

# Read arXiv IDs from file
while read id; do
    echo "Processing $id..."
    axe chop "$id" --format both
    sleep 2  # Rate limiting
done < arxiv_ids.txt

# Show final stats
axe stats --show
```

---

## Tips and Tricks

### 1. Default Format

If you always use markdown, it's the default - no need to specify:
```bash
axe chop paper.pdf  # automatically uses markdown
```

### 2. Quick Current Directory

The dot (`.`) is a shorthand for current directory:
```bash
cd ~/papers
axe chop .
```

### 3. Tab Completion

If your shell supports it, tab completion works:
```bash
axe ch[TAB]  # completes to 'chop'
axe path --[TAB]  # shows --in, --out, --show
```

### 4. Help Anytime

Get help for any command:
```bash
axe --help
axe chop --help
axe path --help
```

### 5. Config Location

All settings stored in `~/.axe_cli/`:
```bash
ls ~/.axe_cli/
# config.json  stats.json
```

View or edit manually:
```bash
cat ~/.axe_cli/config.json
cat ~/.axe_cli/stats.json
```

---

## Troubleshooting Examples

### Check if Installed

```bash
which axe
# Should output: /home/user/.local/bin/axe
```

### Verify Dependencies

```bash
python3 -m pip list | grep -E "arxiv|rich|click"
```

### Test with Help

```bash
axe --help  # If this works, installation is good
```

### Manual Config Check

```bash
cat ~/.axe_cli/config.json
```

### Clear Stats and Start Fresh

```bash
axe stats --reset
rm -rf ~/.axe_cli/stats.json
```

---

## Performance Notes

### Rate Limiting

arXiv has rate limits. AXE CLI includes delays:
- 0.1s between file operations
- Respects arXiv API guidelines
- No manual rate limit configuration needed

### Large Batches

For very large batches (100+ papers):
```bash
# Process in chunks
axe chop papers_1-50/ 
# Wait a bit
axe chop papers_51-100/
```

### Disk Space

Check available space before large operations:
```bash
df -h ~/converted  # Check output directory space
```

---

This covers the majority of use cases for AXE CLI. For more information, see the README.md or run `axe help`.
