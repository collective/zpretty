from importlib.resources import files
from tempfile import TemporaryDirectory
from unittest import TestCase
from zpretty.cli import CLIRunner
from zpretty.prettifier import ZPrettifier
from zpretty.tests.mock import MockCLIRunner
from zpretty.xml import XMLPrettifier
from zpretty.zcml import ZCMLPrettifier

import os


class TestCli(TestCase):
    """Test the cli options"""

    sample_folder_path = files("zpretty.tests") / "original"

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
        html = str(self.sample_folder_path / "sample_html.html")
        xml = str(self.sample_folder_path / "sample_xml.xml")
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
        self.assertEqual(clirunner.choose_prettifier("a.xsd"), XMLPrettifier)
        self.assertEqual(clirunner.choose_prettifier("a.xsl"), XMLPrettifier)
        self.assertEqual(clirunner.choose_prettifier("a.xslt"), XMLPrettifier)
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

        # XML helper extensions should be included by default in recursive scans
        with TemporaryDirectory() as tempdir:
            xsd = os.path.join(tempdir, "schema.xsd")
            xslt = os.path.join(tempdir, "transform.xslt")
            with open(xsd, "w"):
                pass
            with open(xslt, "w"):
                pass
            clirunner = MockCLIRunner(tempdir)
            self.assertListEqual(
                clirunner.good_paths,
                sorted([xsd, xslt]),
            )

    def test_truncated_file_is_refused_and_not_overwritten(self):
        """`zpretty -i` on truncatable XML errors out and leaves the file intact."""
        from unittest import mock

        original = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<recipe>\n  <cake>Sachertorte</cake>\n</recipe>\n"
            "<recipe>\n  <cake>Gugelhupf</cake>\n</recipe>\n"
        )
        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "recipes.xml")
            with open(path, "w") as f:
                f.write(original)
            clirunner = MockCLIRunner("-x", "-i", path)
            with mock.patch("builtins.exit", return_value=None) as mocked:
                clirunner.run()
                mocked.assert_called_once_with(1)
            with open(path) as f:
                self.assertEqual(f.read(), original)
            self.assertListEqual(os.listdir(tmpdir), ["recipes.xml"])

    def test_atomic_write_replaces_content(self):
        """--inplace writes are atomic and leave no temporary file behind."""
        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "f.xml")
            with open(path, "w") as f:
                f.write("OLD")
            CLIRunner._atomic_write(path, "NEW")
            with open(path) as f:
                self.assertEqual(f.read(), "NEW")
            self.assertListEqual(os.listdir(tmpdir), ["f.xml"])

    def test_atomic_write_preserves_original_on_failure(self):
        """A failed --inplace write must leave the original file untouched."""
        from unittest import mock

        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "f.xml")
            with open(path, "w") as f:
                f.write("ORIGINAL")
            with mock.patch("os.replace", side_effect=OSError("boom")):
                with self.assertRaises(OSError):
                    CLIRunner._atomic_write(path, "NEW")
            with open(path) as f:
                self.assertEqual(f.read(), "ORIGINAL")
            self.assertListEqual(os.listdir(tmpdir), ["f.xml"])
