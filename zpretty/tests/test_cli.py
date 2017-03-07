# coding=utf-8
from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.cli import get_parser


class TestCli(TestCase):
    ''' Test the cli options
    '''
    parser = get_parser()

    def test_defaults(self):
        parsed = self.parser.parse_args([])
        self.assertEqual(parsed.file, '-')
        self.assertFalse(parsed.inplace)
        self.assertFalse(parsed.xml)
        self.assertFalse(parsed.zcml)
        self.assertEqual(parsed.encoding, 'utf8')

    def test_short_options(self):
        parsed = self.parser.parse_args(['-i', '-x', '-z'])
        self.assertTrue(all((
            parsed.inplace,
            parsed.xml,
            parsed.zcml,
        )))

    def test_long_options(self):
        parsed = self.parser.parse_args(['--inplace', '--xml', '--zcml'])
        self.assertTrue(all((
            parsed.inplace,
            parsed.xml,
            parsed.zcml,
        )))

    def test_file(self):
        html = resource_filename(
            'zpretty.tests',
            'original/sample_html.html'
        )
        xml = resource_filename(
            'zpretty.tests',
            'original/sample_xml.xml'
        )
        parsed = self.parser.parse_args([html, xml])
        self.assertEqual(
            parsed.file,
            [html, xml],
        )
