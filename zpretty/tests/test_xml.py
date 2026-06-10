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

    def test_sample_mixed_content(self):
        """Full-document idempotency for prose with inline elements.

        On master this fixture is reflowed (each inline element onto its own
        line), so this test makes the change easy to compare against master.
        """
        self.prettify("sample_mixed_content.xml")

    def test_inline_elements_keep_text_flow(self):
        """Empty inline elements in prose must not break the text flow.

        On master the result is reflowed onto several lines.
        """
        observed = XMLPrettifier(
            text=(
                "<recipe>\n"
                "  <p>This <cake_name/> uses <ingredient_count/> ingredients.</p>\n"
                "</recipe>\n"
            )
        )()
        self.assertIn(
            "<p>This <cake_name /> uses <ingredient_count /> ingredients.</p>",
            observed,
        )

    def test_inline_element_with_text_keeps_flow(self):
        """Inline elements that contain text also stay within the prose flow."""
        observed = XMLPrettifier(
            text="<recipe>\n  <p>see the <a>method</a> below</p>\n</recipe>\n"
        )()
        self.assertIn("<p>see the <a>method</a> below</p>", observed)

    def test_single_text_child_is_preserved(self):
        """An element with a single text child keeps it inline (unchanged)."""
        observed = XMLPrettifier(text="<root>\n  <p>just text</p>\n</root>\n")()
        self.assertIn("<p>just text</p>", observed)

    def test_block_content_is_reflowed_one_child_per_line(self):
        """Element-only content laid out with whitespace stays one child per
        line (preservation is limited to real prose, not structural markup)."""
        observed = XMLPrettifier(text="<root>\n  <a/>\n  <b/>\n</root>\n")()
        self.assertIn("\n  <a />\n", observed)
        self.assertIn("\n  <b />\n", observed)

    def test_blank_line_between_block_children_is_not_prose(self):
        """A blank line between block children must not be mistaken for prose;
        the children still reflow, indented. Regression guard for the internal
        blank-line marker being counted as text.
        """
        observed = XMLPrettifier(text="<root>\n  <a/>\n\n  <b/>\n</root>\n")()
        self.assertIn("\n  <a />\n", observed)
        self.assertIn("  <b />", observed)

    def test_br_forces_newline_after(self):
        """A <br/> in mixed content breaks the line after it.

        On the base branch <br/> stays glued to the following text.
        """
        observed = XMLPrettifier(
            text="<recipe><p>Whisk eggs<br/>then fold in flour</p></recipe>\n"
        )()
        self.assertIn("Whisk eggs<br />\n", observed)
        self.assertEqual(observed, XMLPrettifier(text=observed)())

    def test_br_does_not_double_newline(self):
        """A <br/> already followed by a line break gets no extra newline."""
        observed = XMLPrettifier(
            text=(
                "<recipe><step>Sift the flour<br/>\n"
                "    then add sugar</step></recipe>\n"
            )
        )()
        self.assertNotIn("<br />\n\n", observed)
        self.assertEqual(observed, XMLPrettifier(text=observed)())

    def test_br_last_child_no_trailing_blank_line(self):
        """A trailing <br/> does not introduce a blank line before the close."""
        observed = XMLPrettifier(text="<recipe><p>Bake<br/></p></recipe>\n")()
        self.assertIn("<p>Bake<br /></p>", observed)
        self.assertNotIn("<br />\n", observed)

    def test_multiline_recipe_step_renders_as_block(self):
        """Multi-line mixed content renders as a block: open/close tags on
        their own lines, content re-indented to the child level, inline flow
        within a line preserved.

        On the base branch the source indentation is kept verbatim.
        """
        observed = XMLPrettifier(
            text=(
                "<ol>\n"
                "  <li><b>Cream butter and sugar</b><br />Beat until the mixture is\n"
                "              pale and fluffy, about three minutes.</li>\n"
                "</ol>\n"
            )
        )()
        self.assertIn(
            "\n".join(
                (
                    "  <li>",
                    "    <b>Cream butter and sugar</b><br />",
                    "    Beat until the mixture is",
                    "    pale and fluffy, about three minutes.",
                    "  </li>",
                )
            ),
            observed,
        )
        self.assertEqual(observed, XMLPrettifier(text=observed)())

    def test_singleline_mixed_content_stays_inline(self):
        """Single-line mixed content (no <br/>) is not turned into a block."""
        observed = XMLPrettifier(
            text=(
                "<recipe>\n"
                "  <p>fold in the <ingredient>flour</ingredient> gently</p>\n"
                "</recipe>\n"
            )
        )()
        self.assertIn(
            "<p>fold in the <ingredient>flour</ingredient> gently</p>", observed
        )

    def test_multiline_block_normalizes_source_indentation(self):
        """Grotesque source indentation is normalized to the child indent."""
        observed = XMLPrettifier(
            text=(
                "<note>\n"
                "  <p>First line.<br />\n"
                "                       wildly indented second line.</p>\n"
                "</note>\n"
            )
        )()
        self.assertIn("\n    wildly indented second line.\n", observed)
        self.assertNotIn("                       wildly", observed)
        self.assertEqual(observed, XMLPrettifier(text=observed)())

    def test_br_in_single_line_becomes_block(self):
        """A <br/> turns single-line mixed content into a block (A + B)."""
        observed = XMLPrettifier(
            text="<recipe>\n  <step><b>Bake</b><br />until golden</step>\n</recipe>\n"
        )()
        self.assertIn(
            "\n".join(
                ("  <step>", "    <b>Bake</b><br />", "    until golden", "  </step>")
            ),
            observed,
        )
