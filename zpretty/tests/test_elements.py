from bs4 import BeautifulSoup
from unittest import TestCase
from zpretty.elements import PrettyElement


class TestPrettyElements(TestCase):
    """Test basic funtionalities of the PrettyElement class"""

    def get_element(self, text, level=0):
        """Given a text return a PrettyElement"""
        soup = BeautifulSoup(
            "<soup><fake_root>%s</fake_root></soup>" % text, "html.parser"
        )
        return PrettyElement(soup.fake_root.next_element, level)

    def test_comment(self):
        el = self.get_element("<!--a-->")
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_tag())
        self.assertFalse(el.is_text())
        self.assertTrue(el.is_comment())
        self.assertEqual(el.text, "a")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), "")
        self.assertEqual(el(), "<!--a-->")

    def test_text_element(self):
        el = self.get_element("text<ignored_children>")
        self.assertFalse(el.is_comment())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_tag())
        self.assertTrue(el.is_text())
        self.assertEqual(el.text, "text")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), "")
        self.assertEqual(el(), "text")

    def test_empty_element(self):
        el = self.get_element("<root />")
        self.assertFalse(el.is_comment())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_text())
        self.assertTrue(el.is_tag())
        self.assertEqual(el.text, "")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), "")

    def test_empty_element_attributes(self):
        el = self.get_element('<root class="b" />')
        self.assertFalse(el.is_comment())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_text())
        self.assertTrue(el.is_tag())
        self.assertEqual(el.text, "")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), 'class="b"')
        self.assertEqual(el(), '<root class="b"></root>')

    def test_processing_instruction(self):
        el = self.get_element('<?xml version="1.0" encoding="utf-8">')
        self.assertFalse(el.is_tag())
        self.assertFalse(el.is_text())
        self.assertFalse(el.is_doctype())
        self.assertTrue(el.is_processing_instruction())
        self.assertEqual(el.text, 'xml version="1.0" encoding="utf-8"')
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), "")

    def test_doctype(self):
        el = self.get_element("<!DOCTYPE html>")
        self.assertFalse(el.is_tag())
        self.assertFalse(el.is_text())
        self.assertFalse(el.is_processing_instruction())
        self.assertTrue(el.is_doctype())
        self.assertEqual(el.text, "html")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), "")
        el = self.get_element(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
            '"http://www.w3.org/TR/html4/strict.dtd">'
        )
        self.assertEqual(
            el.text,
            'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
            '"http://www.w3.org/TR/html4/strict.dtd"',
        )

    def test_render_text(self):
        el = self.get_element(" a")
        self.assertEqual(el.render_text(), "\na")
        el = self.get_element(" ")
        self.assertEqual(el.render_text(), "\n")
        el = self.get_element("\n")
        self.assertEqual(el.render_text(), "\n")

    def test_get_parent(self):
        el = self.get_element(" a")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getparent().getparent().tag, "soup")
        self.assertIsNone(el.getparent().getparent().getparent())
