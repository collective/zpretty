# coding=utf-8
from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.prettifier import ZPrettifier


class TestZpretty(TestCase):
    """ Test zpretty
    """

    maxDiff = None

    def assertPrettified(self, original, expected, encoding="utf8"):
        """ Check if the original html has been prettified as expected
        """
        if isinstance(expected, tuple):
            expected = u"\n".join(expected)
        prettifier = ZPrettifier(text=original, encoding=encoding)
        observed = prettifier()
        self.assertEqual(observed, expected)

    def prettify(self, filename):
        """ Run prettify on filename and check that the output is equal to
        the file content itself
        """
        resolved_filename = resource_filename("zpretty.tests", "original/%s" % filename)
        prettifier = ZPrettifier(resolved_filename)
        observed = prettifier()
        expected = open(resolved_filename).read()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_format_self_closing_tag(self):
        self.assertPrettified("<tal:test />", u"<tal:test />\n")

    def test_nesting_no_text(self):
        # no attributes
        self.assertPrettified(
            "<root><tal:test /></root>", u"<root><tal:test /></root>\n"
        )

        self.assertPrettified(
            "<root><tal:test /> </root>", u"<root><tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> <tal:test /> </root>", u"<root>\n  <tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> <tal:test /></root>", u"<root>\n  <tal:test /></root>\n"
        )
        self.assertPrettified(
            "<root><tal:test><child /></tal:test></root>",
            u"<root><tal:test><child></child></tal:test></root>\n",
        )

    def test_nesting_with_text(self):
        # no attributes
        self.assertPrettified(
            "<root> a<tal:test /></root>", u"<root>\n  a<tal:test /></root>\n"
        )

        self.assertPrettified(
            "<root>a <tal:test /> </root>", u"<root>a\n  <tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> a <tal:test /> </root>", u"<root>\n  a\n  <tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> a <div /> </root>", u"<root>\n  a\n  <div></div>\n</root>\n"
        )
        self.assertPrettified(
            "<root> a <div /> <div /> </root>",
            u"<root>\n  a\n  <div></div>\n  <div></div>\n</root>\n",
        )
        self.assertPrettified(
            "<root> a <div />\n <div /> </root>",
            u"<root>\n  a\n  <div></div>\n  <div></div>\n</root>\n",
        )
        self.assertPrettified(
            "<root> a <div />\na <div /> </root>",
            u"<root>\n  a\n  <div></div>\na\n  <div></div>\n</root>\n",
        )
        self.assertPrettified(
            "<root> <div>a</div> </root>", u"<root>\n  <div>a</div>\n</root>\n"
        )
        self.assertPrettified(
            "<root> <div>a\n  </div> </root>", u"<root>\n  <div>a\n  </div>\n</root>\n"
        )
        self.assertPrettified("<div><p>a</p></div>", u"<div><p>a</p></div>\n")

    def test_nesting_with_tail(self):
        # no attributes
        self.assertPrettified(
            "<root><p></p><!-- #a -->\n\n<p></p></root>",
            u"<root><p></p><!-- #a -->\n\n  <p></p></root>\n",
        )
        self.assertPrettified(
            "<root><tal:test />a</root>", u"<root><tal:test />a</root>\n"
        )
        self.assertPrettified(
            "<root><tal:test />a </root>", (u"<root><tal:test />a", u"</root>", u"")
        )

        self.assertPrettified(
            "<root><tal:test /> a </root>",
            (u"<root><tal:test />", u"  a", u"</root>", u""),
        )
        self.assertPrettified(
            "<root><tal:test /> a </root>", u"<root><tal:test />\n  a\n</root>\n"
        )

    def test_many_children(self):
        """
        """
        self.assertPrettified(
            u"<root><tal:test /><div></div></root>",
            u"<root><tal:test /><div></div></root>\n",
        )
        self.assertPrettified(
            u"<root><tal:test /> <div></div></root>",
            u"<root><tal:test />\n  <div></div></root>\n",
        )

    def test_valueless_attributes(self):
        """ Test attributes without value
        (hidden, required, data-attributes, ...)
        Some of them are rendered valueless, some other not.
        """
        self.assertPrettified(
            u'<root data-attribute=""></root>', u"<root data-attribute></root>\n"
        )
        self.assertPrettified(u"<root hidden></root>", u"<root hidden></root>\n")
        self.assertPrettified(u"<root selected></root>", u'<root selected=""></root>\n')

    def test_fix_self_closing(self):
        """ Check if open self closing tags are rendered correctly
        """
        self.assertPrettified(u"<input><img><input>", u"<input /><img /><input />\n")
        self.assertPrettified(u"<input><a /><b />", u"<input /><a></a><b></b>\n")
        self.assertPrettified(
            u"<input><a /><b /></input>", u"<input /><a></a><b></b>\n"
        )

    def test_element_repr(self):
        prettifier = ZPrettifier(text="")
        self.assertEqual(repr(prettifier.root), "<pretty:-1:null_tag_name />")

    def test_whitelines_not_stripped(self):
        self.assertPrettified(u"<root>\n</root>", u"<root>\n</root>\n")
        self.assertPrettified(
            u"<root>\n    Hello!   \n</root>", u"<root>\n    Hello!\n</root>\n"
        )

    def test_entities(self):
        self.assertPrettified("<root>&nbsp;</root>", u"<root>&nbsp;</root>\n")

    def test_sample_html(self):
        self.prettify("sample_html.html")

    def test_text_with_markup(self):
        self.prettify("text_with_markup.md")
