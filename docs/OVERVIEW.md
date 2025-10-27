# AXE CLI - AN INTERACTIVE CLI FOR ARXIV

AXE CLI WILL OFFER FUNCTIONS IN TWO FORMATS:

- DIRECT COMMANDS
- INTERACTIVE CLI MENU
- PERSISTENT STATISTICS / PER RUN STATISTICS

## COMMANDS

### CORE
ROOT_CLI: `axe` - Root CLI command, begins all axe_cli syntax commands
    - e.g.:
        - calling `axe` by iteself in the cli will initiate the interactive cli menu
        - Alternatively, you can use the AXE CLI COMMANDS at anytime in the menu to override the interactive menu process
            - For example, if the interactive menu has started and you enter commands `axe chop <path/to/file>`,
                - the chop process will override the interactive cli menu and begin the conversion process on the targeted file
PATH: `path` - command involving setting, viewing, path for arxiv inputs / outputs
    - e.g.:
        - `axe path --in <path/to/file>` - sets and saves the default directory path for the axe config
        - `axe path --show` - prints the current directory path axe cli is pointed at (default is always root folder where axe is called)
        - `axe path --out <path/to/file>` - sets and saves an output directory for converted files
CHOP: `chop` - conversion command for arxiv -> markdown / text
    - e.g.:
        - `axe chop <path/to/file>` - Quick, direct command to convert a file from arxiv to markdown/text from the cli (no interactive menu required)
        - `axe chop .` - converts all files in the current directory from arxiv to text/markdown
        - `axe chop path .` - (REQUIRES PATH TO BE SET FROM THE CONFIG OR USING THE `axe path --set <path/to/default/directory>`)
HELP: `-h`, `help` - self explanatory help menu, for brevity i will only provide one example.
        - `axe chop help` - provids additional information and help for the `chop` commands

### OPTIONS
INPUT: `--in` - assign a command to its variable
    - e.g.:
        - `axe path --in <path/to/directory/>` - sets the default directory path to search, identify and convert files from arxiv
SHOW: `--show` - reveals the set data for a command, variable or option
    - e.g.:
        - `axe path --show` - prints the currently set processing directory path, if no default set in config, or cli, **ALWAYS** default = `root directly axe is called from in the terminal`
        - `axe stats --show` - prints the persistent stats(per run stats print automatically, after each run, no command required)
OUTPUT: `--out` - the output directory or where to save the converted file(s) after processing.
    - e.g.:
        - `axe path --out` - converts all files in the current directory from arxiv to text/markdown

### OPERATORS
ALL: `.` - processes all files found(in the current directory) for arxiv, and converts them
    - e.g.:
        - `axe chop .` - converts all files in the current directory from arxiv to text/markdown
