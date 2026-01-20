from importlib.resources import files
from unittest import TestCase
from zpretty.tests.mock import MockCLIRunner

import argparse


class TestReadme(TestCase):
    """Test zpretty"""

    maxDiff = None

    def extract_usage_from_readme(self):
        """Extract the usage from the documentation"""
        readme_path = files("zpretty").parent / "README.md"
        readme = readme_path.read_text()
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
