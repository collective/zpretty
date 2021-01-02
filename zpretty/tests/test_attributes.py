from unittest import TestCase
from zpretty.attributes import PrettyAttributes


class TestZPrettyAttributess(TestCase):
    """Test zpretty"""

    def assertPrettifiedAttributes(self, attributes, expected, level=0):
        """Check if the attributes are properly sorted and formatted"""
        pretty_attribute = PrettyAttributes(attributes)
        observed = pretty_attribute()
        self.assertEqual(observed, expected)

    def test_no_attributes(self):
        self.assertPrettifiedAttributes({}, "")

    def test_one_attribute(self):
        self.assertPrettifiedAttributes({u"a": "1"}, 'a="1"')

    def test_tal_define(self):
        self.assertPrettifiedAttributes(
            {u"tal:define": "a 1; b 2"},
            "\n".join((u'tal:define="', "  a 1;", "  b 2;", '"')),
        )

    def test_format_attributes_many_attribute(self):
        self.assertPrettifiedAttributes(
            {u"a": "1", "b": "2", "class": "hidden", "tal:define": "a 1; b 2"},
            "\n".join(
                (
                    'class="hidden"',
                    'a="1"',
                    'b="2"',
                    'tal:define="',
                    "  a 1;",
                    "  b 2;",
                    '"',
                )
            ),
        )
