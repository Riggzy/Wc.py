# WC.PY
## A Python script for daily word-counts.

This script was written to provide an easy command-line interface for performing a word-count. It counts the number of words in recently-edited text files and compares them against a previous record.

## History

26/04/2011: Fixed the copyright dedication in the help message - the script is indeed dedicated to the Public Domain. Also, the `default_threshold` is now 2 days, to avoid an issue where writing past midnight resulted in files being ignored when the script is run.

25/04/2011: Added the `init` option to create the `.wordcount` file, so other people can finally use this script. D'oh. Also added a built-in `help` command that prints usage instructions, and fixed some of the phrasing in printed messages.

## Setup

Edit the script and change the `default_path` and `default_threshold` values to your liking.

`default_path` represents the root directory of the text files to be indexed. The script is recursive, so all sub-directories are included.

`default_threshold` defines what constitutes a 'recent file', that is, what files are included in the word count. You should run `wc.py update` as often as you set here, to keep things in sync.

Before you can perform a word count, you'll have to run `wc.py init` to initially create the `.wordcount` file that holds the data.

The script will only index `.txt` files, but this can be changed in the script by editing the appropriate line in the `findRecentFiles` function.

## Usage

`wc.py` shows word counts for each recent file, and a total.

`wc.py raw` prints the total number, by itself.

`wc.py update` records the current word count of all recent files.

`wc.py help` prints these usage instructions.

