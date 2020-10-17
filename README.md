# grump

Grep for Unstructured Multiline Paragraphs

A *multiline paragraph* is a string in which there are no 'empty
lines' - two newlines separated only by whitespace. For example
given `data.txt`:

```
This is
one multiline
paragraph.

This is
another
multiline
paragraph.

This one is too!
```

`grump` takes a file and a list of strings and outputs all multiline
paragraphs of this file containing each string in the list. For
example:

```
$ grump -f data.txt this one
This is
one multiline
paragraph.

This one is too!
```

## Installation

```
python3 -m pip install grump
```

## Usage

```
usage: grump [-h] [-w] [-c] [-f FILENAME] regex [regex ...]

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
grump -f testdata.txt amy fred
grump amy fred < testdata.txt
cat testdata.txt | grump amy fred
grump --file testdata.txt amy fred --word --case-sensitive
grump -f testdata.txt amy fred -w -c
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

* Fork the repository https://github.com/andrewsolomon/grump
* Make some changes
* Update `tests/test_grump.py`
* Make sure tests pass
```
black grump/grump.py
black tests/test_grump.py
pytest
```
* Make a pull request

## Releasing

Give it a new version:
```
bump2version --no-commit --no-tag patch
```

and remove `--no-commit` and `--no-tag` when you're sure. Then

```
git push
git push --tags
```

Note, "patch" indicates a bugfix or minor improvement.

* If there are new, backward compatible features change "patch" to "minor"
* If there are *backward incompatible* changes change "patch" to "major"

Package it:
```
python setup.py clean --all
rm -rf dist/ build/ grump.egg-info/ grump_andrewsolomon.egg-info/
python setup.py sdist bdist_wheel
```

Upload it to test pypi:
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

install it from there:

```
python3 -m pip install --upgrade -i https://test.pypi.org/simple/ grump
```

Then upload it to pypi.org
```
twine upload dist/*
```
