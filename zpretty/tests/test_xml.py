from bs4 import BeautifulSoup
from unittest import TestCase
from zpretty.xml import XMLElement
from zpretty.xml import XMLPrettifier


try:
    from importlib.resources import files

    def resource_filename(package, resource):
        """Get the resource filename for a package and resource."""
        return str(files(package).joinpath(resource))

except ImportError:  # Python < 3.9
    # Python < 3.9
    from pkg_resources import resource_filename


class TestZpretty(TestCase):
    """Test zpretty"""

    maxDiff = None

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
        resolved_filename = resource_filename("zpretty.tests", "original/%s" % filename)
        prettifier = XMLPrettifier(resolved_filename)
        observed = prettifier()
        expected = open(resolved_filename).read()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_newline_between_attributes(self):
        """See #84"""
        element = self.get_element('<one \n foo="bar"\n\n\nbar="foo"\n/>')
        self.assertEqual(element(), '<one bar="foo"\n     foo="bar"\n/>')

    def test_zcml(self):
        self.prettify("sample_xml.xml")

    def test_sample_dtml(self):
        self.prettify("sample_dtml.dtml")

    def test_sample_txt(self):
        self.prettify("sample.txt")
