from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.cli import get_parser

import argparse
import sys


class TestReadme(TestCase):
    """Test zpretty"""

    maxDiff = None

    def extract_usage_from_readme(self):
        """Extract the usage from the documentation"""
        resolved_filename = resource_filename("zpretty", "../README.md")
        with open(resolved_filename) as f:
            readme = f.read()
            if sys.version_info < (3, 9):  # pragma: no cover
                # Small change in the argparse output for Python >= 3.9
                readme = readme.replace("[file ...]", "[file [file ...]]")
        start = readme.index("    zpretty [")
        end = readme.index("\n\nWithout", start)
        return readme[start:end].splitlines()

    def extract_usage_from_parser(self):
        """Ask the parser for the usage and indent it"""
        parser = get_parser()
        # This is needed to keep the 80 lines limit
        parser.formatter_class = lambda prog: argparse.HelpFormatter(prog, width=80)
        # temporarily remove the description
        parser.description = None
        parser_help = parser.format_help()
        start = parser_help.index("zpretty [")
        parser_help = parser_help[start:]

        return ["    {0}".format(x).rstrip() for x in parser_help.splitlines()]

    def test_readme(self):
        observed = self.extract_usage_from_readme()
        expected = self.extract_usage_from_parser()
        self.assertListEqual(observed, expected)
