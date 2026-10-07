from bs4 import BeautifulSoup
from importlib.resources import files
from textwrap import dedent
from unittest import TestCase
from zpretty.prettifier import ContentLossError
from zpretty.xml import XMLElement
from zpretty.xml import XMLPrettifier


class TestZpretty(TestCase):
    """Test zpretty"""

    maxDiff = None

    sample_folder_path = files("zpretty.tests") / "original"

    def get_element(self, text, level=0):
        """Given a text return a XMLElement"""
        soup = BeautifulSoup(
            "<soup><fake_root>%s</fake_root></soup>" % text, "html.parser"
        )
        return XMLElement(soup.fake_root.next_element, level)

    def prettify(self, filename):
        """Run prettify on filename and check that the output is equal to
        the file content itself
        """
        filename_path = self.sample_folder_path / filename
        prettifier = XMLPrettifier(filename_path)
        observed = prettifier()
        expected = filename_path.read_text()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_newline_between_attributes(self):
        """See #84"""
        element = self.get_element('<one \n foo="bar"\n\n\nbar="foo"\n/>')
        self.assertEqual(element(), '<one bar="foo"\n     foo="bar"\n/>')

    def test_prolog_comment_newline(self):
        """Check that a comment after the XML prolog is correctly formatted."""
        expected = dedent("""\
            <?xml version="1.0" encoding="utf-8"?>
            <!-- comment -->
            <parent>
              <child>text</child>
            </parent>
        """)
        template = dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            {comment}
            <parent>
              <child>text</child>
                </parent>
        """)
        for comment in (
            "<!-- comment -->",
            "<!-- comment -->\n",
            "\n<!-- comment -->",
        ):
            original = template.format(comment=comment)
            prettifier = XMLPrettifier(text=original)
            observed = prettifier()
            self.assertEqual(observed, expected, f"Failed for comment: {comment!r}")

    def test_prolog_multiline_comment_newline(self):
        expected = dedent("""\
                <?xml version="1.0" encoding="utf-8"?>
                <!--
                  multiline
                    comment
                -->
                <parent>
                  <child>text</child>
                </parent>
            """)
        template = dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            {comment}
            <parent>
              <child>text</child>
                </parent>
        """)
        for comment in (
            "<!--\n  multiline\n    comment\n-->",
            "\n<!--\n  multiline\n    comment\n-->",
            "<!--\n  multiline\n    comment\n-->\n",
        ):
            original = template.format(comment=comment)
            prettifier = XMLPrettifier(text=original)
            observed = prettifier()
            self.assertEqual(observed, expected, f"Failed for comment: {comment!r}")

    def test_xml(self):
        self.prettify("sample_xml.xml")

    def test_sample_xsd(self):
        self.prettify("sample_xsd.xsd")

    def test_sample_xsl(self):
        self.prettify("sample_xsl.xsl")

    def test_sample_dtml(self):
        self.prettify("sample_dtml.dtml")

    def test_sample_txt(self):
        self.prettify("sample.txt")

    def test_recoverable_xml_is_repaired_not_refused(self):
        """A mismatched closing tag is repaired, not rejected.

        lxml recover mode rewrites ``</frosting>`` to match ``<filling>``
        without losing the text, and that auto-fix must keep working.
        """
        text = "<cake><filling>ganache</frosting></cake>"
        observed = XMLPrettifier(text=text)()
        self.assertIn("ganache", observed)
        self.assertIn("<filling>ganache</filling>", observed)
        self.assertNotIn("</frosting>", observed)

    def test_truncated_xml_is_refused(self):
        """Content after the root element is silently dropped, so we refuse."""
        text = dedent("""\
            <?xml version="1.0" encoding="utf-8"?>
            <recipe>
              <cake>Sachertorte</cake>
            </recipe>
            <recipe>
              <cake>Gugelhupf</cake>
            </recipe>
        """)
        with self.assertRaises(ContentLossError):
            XMLPrettifier(text=text)()

    def test_truncated_file_is_refused(self):
        """A file that would be truncated raises rather than losing a recipe."""
        path = self.sample_folder_path / "truncated_recipe.xml"
        with self.assertRaises(ContentLossError):
            XMLPrettifier(path)()
