# grump

Grep for Unstructured Multiline Paragraphs

A *multiline paragraph* is a string in which there are no
'empty lines' - two newlines separated only by whitespace.

Grump takes a file and a list of strings and outputs all multiline paragraphs
of this file containing each string in the list.

## Installation

```
    python3 -m pip install grump
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
    bump2version major # when there are backward incompatible changes
    bump2version minor # for new backward-compatible features
    bump2version patch # bug fixes and improvements
```

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
    python3 -m pip install -i https://test.pypi.org/simple/ grump
```

Then upload it to pypi.org
```
    twine upload dist/*
```

## References

* [Packaging Projects](https://packaging.python.org/tutorials/packaging-projects/)
* [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

