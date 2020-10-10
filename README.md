# grump

Grep for Unstructured Multiline Paragraphs

A *multiline paragraph* is a string in which there are no
'empty lines' - two newlines separated only by whitespace.

Grump takes a file and a list of strings and outputs all multiline paragraphs
of this file containing each string in the list.

## Installation

```
pip install grump
```

## Usage

```
usage: grump.py [-h] [-w] [-c] [-f FILENAME] regex [regex ...]

Grep for unstructured multiline paragraphs

positional arguments:
  regex                 the string or regular expression to match against

optional arguments:
  -h, --help            show this help message and exit
  -w, --word            only match whole words
  -c, --case-sensitive  Perform case sensitive matching. By default, grump is case insensitive.
  -f FILENAME, --file FILENAME
                        the file to grep (default: STDIN)
```

## Examples

From the CLI

```
$ grump -f testdata.txt amy fred
$ grump amy fred < testdata.txt
$ cat testdata.txt | grump amy fred
$ grump --file testdata.txt amy fred --word --case-sensitive
$ grump -f testdata.txt amy fred -w -c
```

As a module

```
import grump

# with text from textfile.txt
with grump.Grump('textfile.txt', ('amy','fred')) as matches:
    for p in matches:
        print(p)

# with text from STDIN
with grump.Grump(None, ('amy','fred')) as matches:
    for p in matches:
        print(p)

# with non-default matching rules
with grump.Grump(
        'textfile.txt',
        ('amy','fred'),
        case_sensitive=True,
        word=True
    ) as matches:

```

## Contributing

Fork the repository, make some changes, update `tests.py` then run:

```
pip install flake8
flake8 grump.py
```
and if it passes, make a pull request.
