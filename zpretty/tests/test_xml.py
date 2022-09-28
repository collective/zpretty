from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.xml import XMLPrettifier


class TestZpretty(TestCase):
    """Test zpretty"""

    maxDiff = None

    def prettify(self, filename, cdata):
        """Run prettify on filename and check that the output is equal to
        the file content itself
        """
        resolved_filename = resource_filename("zpretty.tests", "original/%s" % filename)
        prettifier = XMLPrettifier(resolved_filename, cdata=cdata)
        observed = prettifier()
        expected = open(resolved_filename).read()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_zcml(self):
        self.prettify("sample_xml.xml", False)

    def test_sample_dtml(self):
        self.prettify("sample_dtml.dtml", False)

    def test_cdata(self):
        self.prettify("sample_cdata.xml", True)
