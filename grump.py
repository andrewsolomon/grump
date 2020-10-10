#!/usr/bin/env python3

__version__ = "0.1.0"

import argparse
import io
import os
import re
import sys


class Grump:

    """
    Note: using context manager as a class to ensure the file handle is
    closed at the end
    https://book.pythontips.com/en/latest/context_managers.html
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f"exc_type: {exc_type}")
            print(f"exc_value: {exc_value}")
            print(f"exc_traceback: {exc_traceback}")
        self.f.close()

    def __init__(self, fname, strings, case_sensitive=False, word=False):
        """
        latin-1 so it doesn't die while reading the file...
        http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html#files-in-an-ascii-compatible-encoding-best-effort-is-acceptable
        """

        try:
            if fname is None:
                """
                self.f = sys.stdin # Chokes on funny characters
                self.f = open(1, 'r', encoding='latin-1')
                    # Ignores piped text  e.g cat foo | grump bar
                """
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

    def get_first_nonempty_line(self):
        while True:
            line = self.f.readline()
            # if we're at the end of the file
            if not line:
                break
            if not re.search(r"^\s*$", line):
                return line
        return False

    def count_and_color_matches(self, blob):
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
            blob, num = reg.subn(rf"{START_MATCH}\1{END_MATCH}", blob, count=0)
            if num == 0:
                return {"matches": 0, "blob": blob}
            num_matches += num

        return {"matches": num_matches, "blob": blob}

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            blob = self.get_first_nonempty_line()
            if not blob:
                raise StopIteration
            while True:
                line = self.f.readline()
                if re.search(r"^\s*$", line):
                    break
                blob += line
            count_match = self.count_and_color_matches(blob)
            if count_match["matches"] > 0:
                return count_match["blob"]


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
        for blob in g:
            print(blob)


if __name__ == "__main__":
    main()
