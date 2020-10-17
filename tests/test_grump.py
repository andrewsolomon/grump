#!/usr/bin/env python3

# https://realpython.com/python-testing/#choosing-a-test-runner
# Run it with:
#  python -m unittest -v tests.TestGrump

import re
import unittest
import os

import grump


class TestGrump(unittest.TestCase):
    def setUp(self):
        self.testdata_file = os.path.dirname(os.path.abspath(__file__)) + "/data.txt"

    def test_default_attrs(self):
        """
        Test that the object attributes are as expected
        """
        # NOTE: we need it wrapped in the "with" so that the object is destroyed and the
        # file doesn't remain open
        with grump.Grump(self.testdata_file, ("blah",)) as g:
            self.assertIsInstance(g, grump.Grump, "It is an instance")
            self.assertFalse(g.word, "By default word is false")
            self.assertFalse(g.case_sensitive, "Case insensitive by default")

    def test_case_insensitive(self):
        """
        Test that by default case matches are case insensitive
        """
        with grump.Grump(self.testdata_file, ("amy", "fred")) as g:
            self.assertIsInstance(g, grump.Grump, "It is an instance")
            self.assertFalse(g.case_sensitive, "Case insensitive by default")
            i = 0
            for blob in g:
                i += 1
                self.assertTrue(re.match("^P[12367]", blob), blob)
            self.assertEqual(i, 5, "Expected number of matches")

    def test_case_sensitive(self):
        """
        Test case sensitive
        """
        with grump.Grump(self.testdata_file, ("Amy", "Fred"), case_sensitive=True) as g:
            i = 0
            for blob in g:
                i += 1
                self.assertTrue(re.match("P6", blob), blob)
            self.assertEqual(i, 1, "Expected number of matches")

    def test_word(self):
        """
        Test word
        """
        with grump.Grump(self.testdata_file, ("amy", "fred"), word=True) as g:
            i = 0
            for blob in g:
                i += 1
                self.assertTrue(re.match("P[1236]", blob), blob)
            self.assertEqual(i, 4, "Expected number of matches")

    def test_whitespace_line(self):
        """
        Check that lines of whitespace separate paragraphs
        """
        # NOTE the trailing comma after 'whitespace' is necessary to
        # prevent it being the tuple of it's characters
        with grump.Grump(self.testdata_file, ("whitespace",)) as g:
            i = 0
            for blob in g:
                i += 1
                self.assertTrue(re.match("P[45]", blob), blob)
            self.assertEqual(i, 2, "Expected number of matches")


if __name__ == "__main__":
    unittest.main()
