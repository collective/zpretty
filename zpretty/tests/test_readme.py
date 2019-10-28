# coding=utf-8
from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.cli import get_parser


class TestReadme(TestCase):
    """ Test zpretty
    """

    def extract_usage_from_readme(self):
        """ Extract the usage from the documentation
        """
        resolved_filename = resource_filename("zpretty", "../README.md")
        readme = open(resolved_filename).read()
        start = readme.index("    zpretty [")
        end = readme.index("\n\nWithout", start)
        return readme[start:end].splitlines()

    def extract_usage_from_parser(self):
        """ Ask the parser for the usage and indent it
        """
        parser = get_parser()
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
