from pkg_resources import resource_filename
from unittest import TestCase
from zpretty.prettifier import ZPrettifier


class TestZpretty(TestCase):
    """Test zpretty"""

    maxDiff = None

    def assertPrettified(self, original, expected, encoding="utf8"):
        """Check if the original html has been prettified as expected"""
        if isinstance(expected, tuple):
            expected = "\n".join(expected)
        prettifier = ZPrettifier(text=original, encoding=encoding)
        self.assertFalse(prettifier.check())
        observed = prettifier()
        self.assertEqual(observed, expected)

    def prettify(self, filename):
        """Run prettify on filename and check that the output is equal to
        the file content itself
        """
        resolved_filename = resource_filename("zpretty.tests", "original/%s" % filename)
        prettifier = ZPrettifier(resolved_filename)
        self.assertTrue(prettifier.check())
        observed = prettifier()
        expected = open(resolved_filename).read()
        self.assertListEqual(observed.splitlines(), expected.splitlines())

    def test_format_self_closing_tag(self):
        self.assertPrettified("<tal:test />", "<tal:test />\n")

    def test_nesting_no_text(self):
        # no attributes
        self.assertPrettified(
            "<root><tal:test /></root>", "<root><tal:test /></root>\n"
        )

        self.assertPrettified(
            "<root><tal:test /> </root>", "<root><tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> <tal:test /> </root>", "<root>\n  <tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> <tal:test /></root>", "<root>\n  <tal:test /></root>\n"
        )
        self.assertPrettified(
            "<root><tal:test><child /></tal:test></root>",
            "<root><tal:test><child></child></tal:test></root>\n",
        )

    def test_nesting_with_text(self):
        # no attributes
        self.assertPrettified(
            "<root> a<tal:test /></root>", "<root>\n  a<tal:test /></root>\n"
        )

        self.assertPrettified(
            "<root>a <tal:test /> </root>", "<root>a\n  <tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> a <tal:test /> </root>", "<root>\n  a\n  <tal:test />\n</root>\n"
        )

        self.assertPrettified(
            "<root> a <div /> </root>", "<root>\n  a\n  <div></div>\n</root>\n"
        )
        self.assertPrettified(
            "<root> a <div /> <div /> </root>",
            "<root>\n  a\n  <div></div>\n  <div></div>\n</root>\n",
        )
        self.assertPrettified(
            "<root> a <div />\n <div /> </root>",
            "<root>\n  a\n  <div></div>\n  <div></div>\n</root>\n",
        )
        self.assertPrettified(
            "<root> a <div />\na <div /> </root>",
            "<root>\n  a\n  <div></div>\na\n  <div></div>\n</root>\n",
        )
        self.assertPrettified(
            "<root> <div>a</div> </root>", "<root>\n  <div>a</div>\n</root>\n"
        )
        self.assertPrettified(
            "<root> <div>a\n  </div> </root>", "<root>\n  <div>a\n  </div>\n</root>\n"
        )
        self.assertPrettified("<div><p>a</p></div>", "<div><p>a</p></div>\n")

    def test_nesting_with_tail(self):
        # no attributes
        self.assertPrettified(
            "<root><p></p><!-- #a -->\n\n<p></p></root>",
            "<root><p></p><!-- #a -->\n\n  <p></p></root>\n",
        )
        self.assertPrettified(
            "<root><tal:test />a</root>", "<root><tal:test />a</root>\n"
        )
        self.assertPrettified(
            "<root><tal:test />a </root>", ("<root><tal:test />a", "</root>", "")
        )

        self.assertPrettified(
            "<root><tal:test /> a </root>",
            ("<root><tal:test />", "  a", "</root>", ""),
        )
        self.assertPrettified(
            "<root><tal:test /> a </root>", "<root><tal:test />\n  a\n</root>\n"
        )

    def test_many_children(self):
        """"""
        self.assertPrettified(
            "<root><tal:test /><div></div></root>",
            "<root><tal:test /><div></div></root>\n",
        )
        self.assertPrettified(
            "<root><tal:test /> <div></div></root>",
            "<root><tal:test />\n  <div></div></root>\n",
        )

    def test_boolean_attributes(self):
        """Test attributes without value
        (hidden, required, data-attributes, ...)
        Some of them are rendered valueless, some other not.
        """
        self.assertPrettified(
            '<root data-attribute=""></root>', "<root data-attribute></root>\n"
        )
        self.assertPrettified("<root hidden></root>", "<root hidden></root>\n")
        self.assertPrettified("<root class></root>", '<root class=""></root>\n')

    def test_fix_self_closing(self):
        """Check if open self closing tags are rendered correctly"""
        self.assertPrettified("<input><img><input>", "<input /><img /><input />\n")
        self.assertPrettified("<input><a /><b />", "<input /><a></a><b></b>\n")
        self.assertPrettified("<input><a /><b /></input>", "<input /><a></a><b></b>\n")

    def test_element_repr(self):
        prettifier = ZPrettifier(text="")
        self.assertEqual(repr(prettifier.root), "<pretty:-1:null_tag_name />")

    def test_whitelines_not_stripped(self):
        self.assertPrettified("<root>\n</root>", "<root>\n</root>\n")
        self.assertPrettified(
            "<root>\n    Hello!   \n</root>", "<root>\n    Hello!\n</root>\n"
        )

    def test_text_close_to_an_element(self):
        self.assertPrettified(
            "<root>\n (<a></a>)\n</root>", "<root>\n  (<a></a>)\n</root>\n"
        )

    def test_elements_with_new_lines(self):
        self.assertPrettified("<root\n></root>", "<root></root>\n")
        self.assertPrettified(
            '<root\na="b"\n\n></root>',
            ('<root a="b"></root>\n'),
        )
        self.assertPrettified(
            '<root\na="b"\n\nc="d"></root>',
            ('<root a="b"\n      c="d"\n></root>\n'),
        )

    def test_entities(self):
        self.assertPrettified("<root>&nbsp;</root>", "<root>&nbsp;</root>\n")

    def test_single_quotes_in_attrs(self):
        self.assertPrettified('<root a="\'" />', '<root a="\'"></root>\n')

    def test_sample_html(self):
        self.prettify("sample_html.html")

    def test_sample_html4(self):
        self.prettify("sample_html4.html")

    def test_sample_pt(self):
        self.prettify("sample_pt.pt")

    def test_text_with_markup(self):
        self.prettify("text_with_markup.md")

    def test_text_file(self):
        self.prettify("sample.txt")
