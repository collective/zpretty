from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.cli import choose_prettifier
from zpretty.cli import get_parser
from zpretty.cli import run
from zpretty.prettifier import ZPrettifier
from zpretty.xml import XMLPrettifier
from zpretty.zcml import ZCMLPrettifier


class TestCli(TestCase):
    """Test the cli options"""

    parser = get_parser()

    def test_defaults(self):
        parsed = self.parser.parse_args([])
        self.assertEqual(parsed.file, "-")
        self.assertFalse(parsed.inplace)
        self.assertFalse(parsed.xml)
        self.assertFalse(parsed.zcml)
        self.assertEqual(parsed.encoding, "utf8")
        self.assertFalse(parsed.check)

    def test_short_options(self):
        parsed = self.parser.parse_args(["-i", "-x", "-z"])
        self.assertTrue(all((parsed.inplace, parsed.xml, parsed.zcml)))

    def test_long_options(self):
        parsed = self.parser.parse_args(["--inplace", "--xml", "--zcml"])
        self.assertTrue(all((parsed.inplace, parsed.xml, parsed.zcml)))

    def test_file(self):
        html = resource_filename("zpretty.tests", "original/sample_html.html")
        xml = resource_filename("zpretty.tests", "original/sample_xml.xml")
        parsed = self.parser.parse_args([html, xml])
        self.assertEqual(parsed.file, [html, xml])

    def test_choose_prettifier(self):
        """Check the for the given options and file the best choice is made"""
        parsed = self.parser.parse_args(["--xml", "--zcml"])
        self.assertEqual(choose_prettifier(parsed, ""), ZCMLPrettifier)
        parsed = self.parser.parse_args(["--xml"])
        self.assertEqual(choose_prettifier(parsed, ""), XMLPrettifier)
        # Without options the extension rules
        parsed = self.parser.parse_args([])
        self.assertEqual(choose_prettifier(parsed, "a.zcml"), ZCMLPrettifier)
        parsed = self.parser.parse_args([])
        self.assertEqual(choose_prettifier(parsed, "a.xml"), XMLPrettifier)
        # The default one is returned if the extension is not recognized
        parsed = self.parser.parse_args([])
        self.assertEqual(choose_prettifier(parsed, "a.txt"), ZPrettifier)

    def test_check(self):
        parsed = self.parser.parse_args(["--check"])
        self.assertTrue(parsed.check)

    def test_run(self):
        # XXX increase coverage by improving the mock
        from unittest import mock

        parser = mock.Mock(
            **{"parse_args.return_value": mock.Mock(encoding="utf8", file=[])}
        )

        with mock.patch("zpretty.cli.get_parser", return_value=parser) as mocked:
            run()
            mocked.assert_called_once()
            parser.parse_args.assert_called_once()

    def test_run_check(self):
        # XXX increase coverage by improving the mock
        from unittest import mock

        parser = mock.Mock(
            **{
                "parse_args.return_value": mock.Mock(
                    zcml=False,
                    check=True,
                    encoding="utf8",
                    file=["zpretty/tests/original/sample_xml.xml"],
                )
            }
        )

        with mock.patch("zpretty.cli.get_parser", return_value=parser):
            with mock.patch("builtins.exit", return_value=parser) as mocked:
                run()
                mocked.assert_not_called()

        parser = mock.Mock(
            **{
                "parse_args.return_value": mock.Mock(
                    check=True,
                    encoding="utf8",
                    file=[resource_filename("zpretty.tests", "broken/broken.xml")],
                )
            }
        )

        with mock.patch("zpretty.cli.get_parser", return_value=parser):
            with mock.patch("builtins.exit", return_value=parser) as mocked:
                run()
                mocked.assert_called_once_with(1)
