from bs4.builder import LXMLTreeBuilderForXML
from bs4.element import Comment
from bs4.element import NavigableString
from logging import getLogger
from zpretty.attributes import PrettyAttributes
from zpretty.constants import ANY_IN
from zpretty.elements import PrettyElement
from zpretty.prettifier import ZPrettifier

logger = getLogger(__name__)


class XMLAttributes(PrettyAttributes):
    """Customized attribute formatter for zcml"""

    _boolean_attributes_are_allowed = False
    _known_boolean_attributes = ()
    _multiline_attributes = ()
    _tal_multiline_attributes = ()
    _xml_attribute_order = ()
    _tal_attribute_order = ()

    def sort_attributes(self, name):
        """Sort ZCML attributes in a consistent way"""
        if name in self._xml_attribute_order:
            return (100 + self._xml_attribute_order.index(name), name)
        return super().sort_attributes(name)


class XMLElement(PrettyElement):
    attribute_klass = XMLAttributes
    preserve_text_whitespace_elements = ANY_IN

    def is_self_closing(self):
        """Is this element self closing?"""
        if not self.is_tag():
            raise ValueError("This is not a tag")
        # Just check if the element has some content.
        return not self.getchildren()

    @property
    def tag(self):
        """Return the tag name"""
        prefix = getattr(self.context, "prefix", "")
        if not prefix:
            return self.context.name
        return f"{prefix}:{self.context.name}"

    @property
    def text(self):
        """Return the text contained in this element (if any)

        Convert the text characters to html entities
        """
        if not isinstance(self.context, NavigableString):
            return ""
        if self.is_comment():
            return self.context
        return self.escaper.substitute_xml(self.context.string)


class XMLPrettifier(ZPrettifier):
    """Prettify according to the ZCML style guide"""

    pretty_element = XMLElement
    builder_class = LXMLTreeBuilderForXML

    def restore_comment_newlines(self, soup):
        """Reinsert top-level newlines between comments and following tags.

        lxml's XML parser can drop pure-whitespace separators in this position,
        which merges the comment and the following tag when rendering.
        """
        for child in list(soup.children):
            if not isinstance(child, Comment):
                continue

            next_sibling = child.next_sibling
            if next_sibling is None:
                continue
            child.insert_after(NavigableString("\n"))

    def get_soup(self, text):
        """Tries to get the soup from the given text

        If the text is not some xml like thing a dummy element will be used to wrap it.
        """
        original_soup = self.text2soup(text)
        if original_soup.is_xml:
            self.restore_comment_newlines(original_soup)
            return original_soup

        markup = "<{null}>{text}</{null}>".format(
            null=self.pretty_element.null_tag_name, text=text
        )
        wrapped_soup = self.text2soup(markup)
        return getattr(wrapped_soup, self.pretty_element.null_tag_name)
