from bs4 import BeautifulSoup
from importlib.resources import files
from textwrap import dedent
from unittest import TestCase
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
