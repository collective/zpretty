from bs4 import BeautifulSoup
from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.zcml import ZCMLAttributes
from zpretty.zcml import ZCMLElement
from zpretty.zcml import ZCMLPrettifier


class TestZpretty(TestCase):
    """Test zpretty"""

    maxDiff = None

    def get_element(self, text, level=0):
        """Given a text return a PrettyElement"""
        soup = BeautifulSoup(
            "<soup><fake_root>%s</fake_root></soup>" % text, "html.parser"
        )
        return ZCMLElement(soup.fake_root.next_element, level)

    def assertPrettifiedAttributes(self, attributes, expected, level=0):
        """Check if the attributes are properly sorted and formatted"""
        if level == 0:
            el = None
        else:
            el = self.get_element("foo", level)
        pretty_attribute = ZCMLAttributes(attributes, el)
        observed = pretty_attribute()
        self.assertEqual(observed, expected)

    def test_zcml_attributes_no_attributes(self):
        self.assertPrettifiedAttributes(ZCMLAttributes({})(), "")
        self.assertPrettifiedAttributes({}, "", level=2)

    def test_zcml_attributes_one_attributes(self):
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"')
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"', level=1)
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"', level=2)

    def test_zcml_attributes_many_attributes(self):
        self.assertPrettifiedAttributes({"a": "1", "b": "2"}, '    a="1"\n    b="2"')
        self.assertPrettifiedAttributes(
            {"a": "1", "b": "2"}, '      a="1"\n      b="2"', level=1
        )
        self.assertPrettifiedAttributes(
            {"a": "1", "b": "2"}, '        a="1"\n        b="2"', level=2
        )

    def test_zcml_self_closing_no_attributes(self):
        element = self.get_element("<zcml />")
        self.assertEqual(element(), "<zcml />")
        element = self.get_element("<zcml />", 1)
        self.assertEqual(element(), "  <zcml />")
        element = self.get_element("<zcml />", 2)
        self.assertEqual(element(), "    <zcml />")

    def test_zcml_self_closing_one_attributes(self):
        element = self.get_element('<zcml \n foo="bar"/>')
        self.assertEqual(element(), '<zcml foo="bar" />')
        element = self.get_element('<zcml \n foo="bar"/>', 1)
        self.assertEqual(element(), '  <zcml foo="bar" />')
        element = self.get_element('<zcml \n foo="bar"/>', 2)
        self.assertEqual(element(), '    <zcml foo="bar" />')

    def test_zcml_self_closing_many_attributes(self):
        element = self.get_element('<zcml \n foo="bar" bar="foo"/>')
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "<zcml",
                    '    bar="foo"',
                    '    foo="bar"',
                    "    />",
                )
            ),
        )
        element = self.get_element('<zcml \n foo="bar" bar="foo"/>', 1)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "  <zcml",
                    '      bar="foo"',
                    '      foo="bar"',
                    "      />",
                )
            ),
        )
        element = self.get_element('<zcml \n foo="bar" bar="foo"/>', 2)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "    <zcml",
                    '        bar="foo"',
                    '        foo="bar"',
                    "        />",
                )
            ),
        )

    def test_for_attribute_single_attribute(self):
        element = self.get_element('<zcml \n for="foo"/>')
        self.assertEqual(element(), '<zcml for="foo" />')
        element = self.get_element('<zcml \n for="foo"/>', 1)
        self.assertEqual(element(), '  <zcml for="foo" />')
        element = self.get_element('<zcml \n for="foo"/>', 2)
        self.assertEqual(element(), '    <zcml for="foo" />')

        element = self.get_element('<zcml \n for="foo bar"/>')
        self.assertEqual(
            element(),
            "\n".join(
                (
                    '<zcml for="foo',
                    '           bar" />',
                )
            ),
        )

        element = self.get_element('<zcml \n for="foo bar"/>', 1)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    '  <zcml for="foo',
                    '             bar" />',
                )
            ),
        )

        element = self.get_element('<zcml \n for="foo bar"/>', 2)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    '    <zcml for="foo',
                    '               bar" />',
                )
            ),
        )

    def test_for_attribute_multiple_attribute(self):
        element = self.get_element('<zcml \n for="foo" handler="bar" />')
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "<zcml",
                    '    for="foo"',
                    '    handler="bar"',
                    "    />",
                )
            ),
        )
        element = self.get_element('<zcml \n for="foo" handler="bar" />', 1)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "  <zcml",
                    '      for="foo"',
                    '      handler="bar"',
                    "      />",
                )
            ),
        )
        element = self.get_element('<zcml \n for="foo" handler="bar" />', 2)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "    <zcml",
                    '        for="foo"',
                    '        handler="bar"',
                    "        />",
                )
            ),
        )

        element = self.get_element('<zcml \n for="foo bar" handler="bar" />')
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "<zcml",
                    '    for="foo',
                    '         bar"',
                    '    handler="bar"',
                    "    />",
                )
            ),
        )
        element = self.get_element('<zcml \n for="foo bar" handler="bar" />', 1)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "  <zcml",
                    '      for="foo',
                    '           bar"',
                    '      handler="bar"',
                    "      />",
                )
            ),
        )
        element = self.get_element('<zcml \n for="foo bar" handler="bar" />', 2)
        self.assertEqual(
            element(),
            "\n".join(
                (
                    "    <zcml",
                    '        for="foo',
                    '             bar"',
                    '        handler="bar"',
                    "        />",
                )
            ),
        )

    def prettify(self, filename):
        """Run prettify on filename and check that the output is equal to
        the file content itself
        """
        resolved_filename = resource_filename("zpretty.tests", "original/%s" % filename)
        prettifier = ZCMLPrettifier(resolved_filename)
        observed = prettifier()
        expected = open(resolved_filename).read()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_zcml(self):
        self.prettify("sample.zcml")
