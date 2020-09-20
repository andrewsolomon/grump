#!/usr/bin/env python3

# https://realpython.com/python-testing/#choosing-a-test-runner
# Run it with:
# python -m unittest -v tests.TestGrump

import unittest
import tempfile
import os

import grump


class TestGrump(unittest.TestCase):
    def setUp(self):
        self.strings = ('TEST A', 'TEST B')
        self.tf = tempfile.NamedTemporaryFile(delete=False)
        self.tf.write(b'Hello world!')
        self.test_filename = self.tf.name
        self.tf.close()

    def test_default_attrs(self):
        """
        Test that the object attributes are as expected
        """
        # NOTE: we need it wrapped in the "with" so that the object is destroyed and the
        # file doesn't remain open
        with grump.Grump(self.tf.name, self.strings) as g:
            self.assertIsInstance(g, grump.Grump, "It is an instance")
            self.assertEqual(g.strings, self.strings, "The strings have been stored")
            self.assertFalse(g.word, 'By default word is false')
            self.assertFalse(g.case_sensitive, 'By default case_sensitive is false')

    def tearDown(self):
        os.unlink(self.test_filename)


if __name__ == '__main__':
    unittest.main()

