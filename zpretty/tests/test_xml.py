# coding=utf-8
from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.xml import XMLPrettifier


class TestZpretty(TestCase):
    """ Test zpretty
    """

    maxDiff = None

    def prettify(self, filename):
        """ Run prettify on filename and check that the output is equal to
        the file content itself
        """
        resolved_filename = resource_filename("zpretty.tests", "original/%s" % filename)
        prettifier = XMLPrettifier(resolved_filename)
        observed = prettifier()
        expected = open(resolved_filename).read()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_zcml(self):
        self.prettify("sample_xml.xml")
