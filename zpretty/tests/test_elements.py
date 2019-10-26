# coding=utf-8
from bs4 import BeautifulSoup
from unittest import TestCase
from zpretty.elements import PrettyElement


class TestPrettyElements(TestCase):
    """ Test basic funtionalities of the PrettyElement class
    """

    def get_element(self, text):
        """ Given a text return a PrettyElement
        """
        soup = BeautifulSoup(
            u"<soup><fake_root>%s</fake_root></soup>" % text, "html.parser"
        )
        return PrettyElement(soup.fake_root.next_element)

    def test_comment(self):
        el = self.get_element("<!--a-->")
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_tag())
        self.assertFalse(el.is_text())
        self.assertTrue(el.is_comment())
        self.assertEqual(el.text, u"a")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), u"")
        self.assertEqual(el(), u"<!--a-->")

    def test_text_element(self):
        el = self.get_element("text<ignored_children>")
        self.assertFalse(el.is_comment())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_tag())
        self.assertTrue(el.is_text())
        self.assertEqual(el.text, u"text")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), u"")
        self.assertEqual(el(), u"text")

    def test_empty_element(self):
        el = self.get_element("<root />")
        self.assertFalse(el.is_comment())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_text())
        self.assertTrue(el.is_tag())
        self.assertEqual(el.text, u"")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), u"")

    def test_empty_element_attributes(self):
        el = self.get_element('<root class="b" />')
        self.assertFalse(el.is_comment())
        self.assertFalse(el.is_doctype())
        self.assertFalse(el.is_processing_instruction())
        self.assertFalse(el.is_text())
        self.assertTrue(el.is_tag())
        self.assertEqual(el.text, u"")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), u'class="b"')
        self.assertEqual(el(), u'<root class="b"></root>')

    def test_processing_instruction(self):
        el = self.get_element(u'<?xml version="1.0" encoding="utf-8">')
        self.assertFalse(el.is_tag())
        self.assertFalse(el.is_text())
        self.assertFalse(el.is_doctype())
        self.assertTrue(el.is_processing_instruction())
        self.assertEqual(el.text, u'xml version="1.0" encoding="utf-8"')
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), u"")

    def test_doctype(self):
        el = self.get_element(u"<!DOCTYPE html>")
        self.assertFalse(el.is_tag())
        self.assertFalse(el.is_text())
        self.assertFalse(el.is_processing_instruction())
        self.assertTrue(el.is_doctype())
        self.assertEqual(el.text, u"html")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getchildren(), [])
        self.assertEqual(el.attributes(), u"")
        el = self.get_element(
            u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
            u'"http://www.w3.org/TR/html4/strict.dtd">'
        )
        self.assertEqual(
            el.text,
            u'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
            u'"http://www.w3.org/TR/html4/strict.dtd"',
        )

    def test_render_text(self):
        el = self.get_element(" a")
        self.assertEqual(el.render_text(), u"\na")
        el = self.get_element(" ")
        self.assertEqual(el.render_text(), u"\n")
        el = self.get_element("\n")
        self.assertEqual(el.render_text(), u"\n")

    def test_get_parent(self):
        el = self.get_element(" a")
        self.assertEqual(el.getparent().tag, "fake_root")
        self.assertEqual(el.getparent().getparent().tag, "soup")
        self.assertIsNone(el.getparent().getparent().getparent())
