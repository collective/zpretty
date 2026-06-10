from bs4 import BeautifulSoup
from importlib.resources import files
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

    def test_two_blank_lines_between_blocks_collapse_to_one(self):
        """Two blank lines between sibling recipe sections collapse to one."""
        observed = XMLPrettifier(
            text=(
                "<recipe>\n"
                "  <section>Sponge</section>\n"
                "\n"
                "\n"
                "  <section>Buttercream</section>\n"
                "</recipe>\n"
            )
        )()
        self.assertIn(
            "<section>Sponge</section>\n\n  <section>Buttercream</section>",
            observed,
        )
        self.assertNotIn("</section>\n\n\n", observed)
        self.assertEqual(observed, XMLPrettifier(text=observed)())

    def test_single_blank_line_between_blocks_is_kept(self):
        """A single blank line between sections is preserved."""
        observed = XMLPrettifier(
            text=(
                "<recipe>\n"
                "  <section>Sponge</section>\n"
                "\n"
                "  <section>Glaze</section>\n"
                "</recipe>\n"
            )
        )()
        self.assertIn(
            "<section>Sponge</section>\n\n  <section>Glaze</section>", observed
        )

    def test_cdata_blank_lines_stay_verbatim(self):
        """Blank lines inside CDATA (the secret recipe) are significant."""
        observed = XMLPrettifier(
            text=(
                "<recipe><method>"
                "<![CDATA[Cream butter\n\n\nfold in flour]]>"
                "</method></recipe>\n"
            )
        )()
        self.assertIn("<![CDATA[Cream butter\n\n\nfold in flour]]>", observed)
