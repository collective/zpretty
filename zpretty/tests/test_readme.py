from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.tests.mock import MockCLIRunner

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
                readme = readme.replace("[paths ...]", "[paths [paths ...]]")
            if sys.version_info < (3, 10):  # pragma: no cover
                # Small change in the argparse output for Python >= 3.10
                readme = readme.replace("options:", "optional arguments:")
        start = readme.index("zpretty [")
        end = readme.index("```", start)
        # Take all the lines ignoring whitespaces
        return [x.strip() for x in readme[start:end].splitlines()]

    def extract_usage_from_parser(self):
        """Ask the parser for the usage and indent it"""
        parser = MockCLIRunner().parser
        # This is needed to keep the 100 lines limit
        parser.formatter_class = lambda prog: argparse.HelpFormatter(prog, width=80)
        # temporarily remove the description
        parser.description = None
        parser_help = parser.format_help()
        start = parser_help.index("zpretty [")
        parser_help = parser_help[start:]
        # Take all the lines ignoring whitespaces
        return [x.strip() for x in parser_help.splitlines()]

    def test_readme(self):
        observed = self.extract_usage_from_readme()
        expected = self.extract_usage_from_parser()
        self.assertListEqual(observed, expected)
