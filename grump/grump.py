#!/usr/bin/env python3

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


As a module::

    import grump

    # with text from textfile.txt
    with grump.Grump('textfile.txt', ('amy','fred')) as matches:
        for p in matches:
            print(p)

    # with text from STDIN - replace filename with None
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

"""

__version__ = "0.0.6"

import argparse
import io
import os
import re
import sys


class Grump:
    """An iterator for finding grump-matching paragraphs"""


    def __init__(self, fname, strings, case_sensitive=False, word=False):
        """
        Parameters
        ----------
        fname: str, optional
            Name of the file to be parsed, or None for STDIN

        strings: list[str]
            list (or tuple) of strings or regular expressions

        case_sensitive: bool
            default False

        word: bool
            default False
        """


        try:
            if fname is None:
                self.f = io.open(sys.stdin.fileno(), "r", encoding="latin-1")
            else:
                self.f = open(fname, "r", encoding="latin-1")
            self.strings = strings
            self.case_sensitive = case_sensitive
            self.word = word
            self.do_color = sys.stdout.isatty()
        except IsADirectoryError:
            print(f"Error: {fname} is a directory")
            sys.exit(2)
        except PermissionError:
            print(f"Error: File {fname} not readable")
            sys.exit(2)
        except FileNotFoundError:
            print(f"Error: File {fname} not found")
            sys.exit(2)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f"exc_type: {exc_type}")
            print(f"exc_value: {exc_value}")
            print(f"exc_traceback: {exc_traceback}")
        self.f.close()

    def __get_first_nonempty_line(self):
        while True:
            line = self.f.readline()
            if not line:
                break
            if not re.search(r"^\s*$", line):
                return line
        return False

    def __count_and_color_matches(self, paragraph):
        flags = re.MULTILINE
        if not self.case_sensitive:
            flags |= re.IGNORECASE

        START_MATCH = END_MATCH = ""
        if self.do_color:
            START_MATCH = "\033[92m"
            END_MATCH = "\033[0m"
        num_matches = 0
        for str in self.strings:
            reg = (
                re.compile(rf"\b({str})\b", flags)
                if self.word
                else re.compile(rf"({str})", flags)
            )
            paragraph, num = reg.subn(rf"{START_MATCH}\1{END_MATCH}", paragraph, count=0)
            if num == 0:
                return {"matches": 0, "paragraph": paragraph}
            num_matches += num

        return {"matches": num_matches, "paragraph": paragraph}

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            paragraph = self.__get_first_nonempty_line()
            if not paragraph:
                raise StopIteration
            while True:
                line = self.f.readline()
                if re.search(r"^\s*$", line):
                    break
                paragraph += line
            count_match = self.__count_and_color_matches(paragraph)
            if count_match["matches"] > 0:
                return count_match["paragraph"]


def get_params() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Grep for unstructured multiline paragraphs",
    )
    parser.add_argument(
        "-w", "--word", action="store_true", dest="word", help="only match whole words"
    )
    parser.add_argument(
        "-c",
        "--case-sensitive",
        action="store_true",
        dest="case_sensitive",
        help="match case sensitively",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        type=str,
        required=False,
        dest="file",
        metavar="FILENAME",
        help="the file to grep (default: STDIN)",
    )
    parser.add_argument(
        "string",
        action="store",
        metavar="regex",
        nargs="+",
        help="the string or regular expression to match against",
    )
    return parser.parse_args()


def main() -> None:
    params = get_params()
    with Grump(
        params.file,
        params.string,
        case_sensitive=params.case_sensitive,
        word=params.word,
    ) as g:
        for paragraph in g:
            print(paragraph)


if __name__ == "__main__":
    main()
