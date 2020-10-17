"""Grep for Unstructured Multiline Paragraphs

A *multiline paragraph* is a string in which there are no 'empty
lines' - two newlines separated only by whitespace.

`grump` takes a file and a list of strings. It then outputs all
multiline paragraphs of the file containing every string in the
list.

`grump` can also be imported as a module.

Examples
--------

From the CLI::

    grump -f testdata.txt amy fred
    grump amy fred < testdata.txt
    cat testdata.txt | grump amy fred
    grump --file testdata.txt amy fred --word --case-sensitive
    grump -f testdata.txt amy fred -w -c
    grump -f testdata.txt amy 'f.*d' -w -c


For use as a module see::

    python3 -m pydoc grump.Grump

"""

__version__ = "0.0.12"

from .grump import Grump

