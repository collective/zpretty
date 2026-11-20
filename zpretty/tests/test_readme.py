from importlib.resources import files
from unittest import TestCase
from zpretty.tests.mock import MockCLIRunner

import argparse
import re


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

    def extract_pinned_versions_from_readme(self):
        """Extract the versions pinned in the CI examples"""
        readme_path = files("zpretty").parent / "README.md"
        readme = readme_path.read_text()
        github = re.search(r"collective/zpretty/\.github/actions/zpretty@(\S+)", readme)
        gitlab = re.search(
            r"collective/zpretty/([^/\s]+)/gitlab/zpretty\.gitlab-ci\.yml", readme
        )
        return github.group(1), gitlab.group(1)

    def extract_versions_from_history(self):
        """Return the topmost and the latest released version from HISTORY.md"""
        history_path = files("zpretty").parent / "HISTORY.md"
        entries = re.findall(
            r"^## (\d\S*) \(([^)]+)\)", history_path.read_text(), re.MULTILINE
        )
        released = [version for version, date in entries if date != "unreleased"]
        return entries[0][0], released[0]

    def test_ci_examples_pin_a_current_release(self):
        """Both CI examples must pin the same version, and it must be the
        latest released or the upcoming one, so the README cannot silently
        fall a release behind.
        """
        github, gitlab = self.extract_pinned_versions_from_readme()
        self.assertEqual(github, gitlab)
        topmost, latest_released = self.extract_versions_from_history()
        self.assertIn(github, (topmost, latest_released))
