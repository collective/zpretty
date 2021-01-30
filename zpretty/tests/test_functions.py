from unittest import TestCase
from zpretty.text import endswith_whitespace
from zpretty.text import lstrip_first_line
from zpretty.text import rstrip_last_line
from zpretty.text import startswith_whitespace


class TestFunctions(TestCase):
    """Test functions used by zpretty"""

    def test_lstrip_first_line_oneline(self):
        self.assertEqual(lstrip_first_line(" a"), "a")

    def test_lstrip_first_line_twolines(self):
        self.assertEqual(lstrip_first_line(" a \n b"), ("a \n b"))

    def test_rstrip_larst_line_oneline(self):
        self.assertEqual(rstrip_last_line("a"), "a")

    def test_rstrip_larst_line_twoline(self):
        self.assertEqual(rstrip_last_line("a\n b "), ("a\n b"))

    def test_none(self):
        self.assertEqual(lstrip_first_line(None), None)
        self.assertEqual(rstrip_last_line(None), None)
        self.assertFalse(endswith_whitespace(None))
        self.assertFalse(startswith_whitespace(None))
