# coding=utf-8
from unittest import TestCase
from zpretty.attributes import PrettyAttributes


class TestZPrettyAttributess(TestCase):
    """ Test zpretty
    """

    def assertPrettifiedAttributes(self, attributes, expected, level=0):
        """ Check if the attributes are properly sorted and formatted
        """
        pretty_attribute = PrettyAttributes(attributes)
        observed = pretty_attribute()
        self.assertEqual(observed, expected)

    def test_no_attributes(self):
        self.assertPrettifiedAttributes({}, u"")

    def test_one_attribute(self):
        self.assertPrettifiedAttributes({u"a": u"1"}, u'a="1"')

    def test_tal_define(self):
        self.assertPrettifiedAttributes(
            {u"tal:define": u"a 1; b 2"},
            u"\n".join((u'tal:define="', u"  a 1;", u"  b 2;", u'"')),
        )

    def test_format_attributes_many_attribute(self):
        self.assertPrettifiedAttributes(
            {u"a": u"1", u"b": u"2", u"class": u"hidden", u"tal:define": u"a 1; b 2"},
            u"\n".join(
                (
                    u'class="hidden"',
                    u'a="1"',
                    u'b="2"',
                    u'tal:define="',
                    u"  a 1;",
                    u"  b 2;",
                    u'"',
                )
            ),
        )
