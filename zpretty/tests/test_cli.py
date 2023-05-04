from pkg_resources import resource_filename
from tempfile import TemporaryDirectory
from unittest import TestCase
from zpretty.prettifier import ZPrettifier
from zpretty.tests.mock import MockCLIRunner
from zpretty.xml import XMLPrettifier
from zpretty.zcml import ZCMLPrettifier

import os


class TestCli(TestCase):
    """Test the cli options"""

    def test_defaults(self):
        config = MockCLIRunner().config
        self.assertEqual(config.paths, "-")
        self.assertFalse(config.inplace)
        self.assertFalse(config.xml)
        self.assertFalse(config.zcml)
        self.assertEqual(config.encoding, "utf8")
        self.assertFalse(config.check)

    def test_short_options(self):
        config = MockCLIRunner("-i", "-x", "-z").config
        self.assertTrue(all((config.inplace, config.xml, config.zcml)))

    def test_long_options(self):
        config = MockCLIRunner("--inplace", "--xml", "--zcml").config
        self.assertTrue(all((config.inplace, config.xml, config.zcml)))

    def test_file(self):
        html = resource_filename("zpretty.tests", "original/sample_html.html")
        xml = resource_filename("zpretty.tests", "original/sample_xml.xml")
        config = MockCLIRunner(html, xml).config
        self.assertEqual(config.paths, [html, xml])

    def test_stdin(self):
        clirunner = MockCLIRunner()
        self.assertListEqual(clirunner.good_paths, ["-"])

    def test_broken_file_path(self):
        with TemporaryDirectory() as tmpdir:
            bad_path = os.path.join(tmpdir, "bad path")
            good_path = os.path.join(tmpdir, "good path")

            with open(good_path, "w") as f:
                f.write("I do exist")

            clirunner = MockCLIRunner(bad_path, good_path)
            self.assertListEqual(clirunner.good_paths, [good_path])

    def test_choose_prettifier(self):
        """Check the for the given options and file the best choice is made"""
        clirunner = MockCLIRunner("--xml", "--zcml")
        self.assertEqual(clirunner.choose_prettifier(""), ZCMLPrettifier)

        clirunner = MockCLIRunner("--xml")
        self.assertEqual(clirunner.choose_prettifier(""), XMLPrettifier)

        # Without options the extension rules
        clirunner = MockCLIRunner()
        self.assertEqual(clirunner.choose_prettifier("a.zcml"), ZCMLPrettifier)
        self.assertEqual(clirunner.choose_prettifier("a.xml"), XMLPrettifier)
        # The default one is returned if the extension is not recognized
        self.assertEqual(clirunner.choose_prettifier("a.txt"), ZPrettifier)

    def test_check(self):
        config = MockCLIRunner("--check").config
        self.assertTrue(config.check)

    def test_run_check(self):
        # XXX increase coverage by improving the mock
        from unittest import mock

        clirunner = MockCLIRunner("--check", "zpretty/tests/original/sample_xml.xml")
        with mock.patch("builtins.exit", return_value=None) as mocked:
            clirunner.run()
            mocked.assert_not_called()

        clirunner = MockCLIRunner("--check", "broken/broken.xml")

        with mock.patch("builtins.exit", return_value=None) as mocked:
            clirunner.run()
            mocked.assert_called_once_with(1)

    def test_good_paths(self):
        """Test the good_paths property"""
        clirunner = MockCLIRunner()
        self.assertListEqual(clirunner.good_paths, ["-"])

        clirunner = MockCLIRunner("zpretty/tests/original/sample_xml.xml")
        self.assertListEqual(
            clirunner.good_paths, ["zpretty/tests/original/sample_xml.xml"]
        )

        clirunner = MockCLIRunner("broken/broken.xml")
        self.assertListEqual(clirunner.good_paths, [])

        clirunner = MockCLIRunner(
            "broken/broken.xml", "zpretty/tests/original/sample_xml.xml"
        )
        self.assertListEqual(
            clirunner.good_paths, ["zpretty/tests/original/sample_xml.xml"]
        )

        clirunner = MockCLIRunner("zpretty/tests", "--include", "broken")
        self.assertListEqual(
            clirunner.good_paths,
            [
                "zpretty/tests/broken/broken.xml",
            ],
        )

        clirunner = MockCLIRunner(
            "zpretty/tests", "--include", "broken", "--exclude", "broken"
        )
        self.assertListEqual(clirunner.good_paths, [])

        clirunner = MockCLIRunner(
            "zpretty/tests/include-exclude",
        )
        self.assertListEqual(
            clirunner.good_paths,
            [
                "zpretty/tests/include-exclude/foo/bar/bar.html",
                "zpretty/tests/include-exclude/foo/bar/bar.pt",
                "zpretty/tests/include-exclude/foo/bar/bar.xml",
                "zpretty/tests/include-exclude/foo/bar/bar.zcml",
                "zpretty/tests/include-exclude/foo/bar/foo.html",
                "zpretty/tests/include-exclude/foo/bar/foo.pt",
                "zpretty/tests/include-exclude/foo/bar/foo.xml",
                "zpretty/tests/include-exclude/foo/bar/foo.zcml",
            ],
        )

        clirunner = MockCLIRunner(
            "zpretty/tests/include-exclude", "--extend-exclude", "bar/foo"
        )
        self.assertListEqual(
            clirunner.good_paths,
            [
                "zpretty/tests/include-exclude/foo/bar/bar.html",
                "zpretty/tests/include-exclude/foo/bar/bar.pt",
                "zpretty/tests/include-exclude/foo/bar/bar.xml",
                "zpretty/tests/include-exclude/foo/bar/bar.zcml",
            ],
        )

        clirunner = MockCLIRunner(
            "zpretty/tests/include-exclude",
            "--include",
            "pt$",
            "--extend-exclude",
            "bar/foo",
        )
        self.assertListEqual(
            clirunner.good_paths,
            [
                "zpretty/tests/include-exclude/foo/bar/bar.pt",
            ],
        )

        clirunner = MockCLIRunner("zpretty/tests/include-exclude", "--exclude", "foo")
        self.assertListEqual(
            clirunner.good_paths,
            [
                "zpretty/tests/include-exclude/.venv/bar.html",
                "zpretty/tests/include-exclude/.venv/bar.pt",
                "zpretty/tests/include-exclude/.venv/bar.xml",
                "zpretty/tests/include-exclude/.venv/bar.zcml",
                "zpretty/tests/include-exclude/venv/bar.html",
                "zpretty/tests/include-exclude/venv/bar.pt",
                "zpretty/tests/include-exclude/venv/bar.xml",
                "zpretty/tests/include-exclude/venv/bar.zcml",
            ],
        )

        clirunner = MockCLIRunner(
            "zpretty/tests/include-exclude", "--exclude", "(foo|bar)"
        )
        self.assertListEqual(
            clirunner.good_paths,
            [],
        )

        with TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, "foo.pt"), "w"):
                pass
            clirunner = MockCLIRunner(
                tempdir,
                "--include",
                "*",
                "--exclude",
                "+",
                "--extend-exclude",
                "[a-0]",
            )
            self.assertListEqual(
                clirunner.good_paths,
                [f"{tempdir}/foo.pt"],
            )
            self.assertListEqual(
                clirunner.errors,
                [
                    "Invalid regular expression for --exclude: '+'",
                    "Invalid regular expression for --extend-exclude: '[a-0]'",
                    "Invalid regular expression for --include: '*'",
                ],
            )
