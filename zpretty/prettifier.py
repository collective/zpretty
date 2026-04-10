from bs4 import BeautifulSoup
from bs4.element import Doctype
from bs4.element import ProcessingInstruction
from bs4.element import Tag
from logging import getLogger
from uuid import uuid4
from zpretty.elements import PrettyElement

import fileinput
import re

logger = getLogger(__name__)


class ZPrettifier:
    """Wraps and renders some text that may contain xml like stuff"""

    pretty_element = PrettyElement
    parser = "html.parser"
    builder = None
    _end_with_newline = True
    _newlines_marker = f"new-line-{str(uuid4())}"
    _ampersand_marker = str(uuid4())
    _cdata_marker = str(uuid4())
    _cdata_pattern = re.compile(r"<!\[CDATA\[(.*?)\]\]>", re.DOTALL)
    _doctype_marker = f"<!DOCTYPE foo-{str(uuid4())}>"
    _doctype_pattern = re.compile(
        r"(<!DOCTYPE[^>[]*(\[[^]]*\])?>)", re.IGNORECASE | re.DOTALL
    )
    _rcdata_tags = ("title", "textarea")
    _cdatas = []
    _doctype = None

    def __init__(self, filename="", text="", encoding="utf8"):
        """Create a prettifier instance taking the contents
        from a text or a filename
        """
        self._entity_mapping = {}
        self.encoding = encoding
        self.filename = filename
        if self.filename:
            text = "".join(fileinput.input([filename]))
        if not isinstance(text, str):
            text = text.decode(self.encoding)
        self.original_text = text
        self.text = self._prepare_text()
        soup = self.get_soup(self.text)
        # Workaround for https://github.com/collective/zpretty/issues/116
        # restore the ampersands
        # in the attributes so that bogus ones can be escaped
        for el in soup.descendants:
            attrs = getattr(el, "attrs", {})
            for key, value in attrs.items():
                if self._ampersand_marker in value:
                    attrs[key] = value.replace(self._ampersand_marker, "&")

        if self.parser == "html.parser":
            # Page templates are parsed with the html.parser,
            # but can contain invalid markup inside RCDATA tags,
            # see https://github.com/collective/zpretty/issues/198
            self.fix_rcdata_markup(soup)

        self.soup = soup

        # Cleanup all spurious self._newlines_marker attributes, see #35
        key = self._newlines_marker.partition("=")[0]
        for el in self.soup.find_all(attrs={key: ""}):
            el.attrs.pop(key, None)

        self.root = self.pretty_element(self.soup, -1)

    def fix_rcdata_markup(self, soup):
        """Parse markup-like text inside RCDATA tags as child nodes.

        In page templates we might have elements inside these fields,
        e.g. inside a <title> or <textarea>.
        The html.parser used by BeautifulSoup escapes the markup inside these tags
        and does not parse it as tags, but we want to prettify it as well.

        This method applies a workaround for this problem,
        by prettifying the content of these tags as if it were an XML fragment
        and then replacing the content of the tag with the prettified version.

        Then the rcdata elements content will be rendered as it is.
        """
        for tag in soup.find_all(self._rcdata_tags):
            raw_content = "".join(str(node) for node in tag.contents)

            null_tag_name = self.pretty_element.null_tag_name
            fragment_soup = BeautifulSoup(
                f"<{null_tag_name}>{raw_content}</{null_tag_name}>",
                self.parser,
            )
            fragment_root = getattr(fragment_soup, null_tag_name, None)
            if not fragment_root:
                continue

            parsed_children = list(fragment_root.children)
            # Check if the tag contains some markup like text,
            # if not we can skip it and avoid to mess with the content
            if not any(isinstance(child, Tag) for child in parsed_children):
                continue

            # Replace the content of the tag with the parsed prettified children
            tag.clear()
            for child in parsed_children:
                tag.append(child)

    def _prepare_text(self):
        """This tweaks the text passed to the prettifier
        to overcome some limitations of the BeautifulSoup parser
        that wants to strip what he does not understand
        (e.g. CDATAs or funny entities).
        """
        text = self.original_text
        self._cdatas = re.findall(self._cdata_pattern, text)
        try:
            self._doctype = self._doctype_pattern.search(text).group(0)
        except AttributeError:
            # No match
            pass
        text = re.sub(self._cdata_pattern, self._cdata_marker, text)
        text = re.sub(self._doctype_pattern, self._doctype_marker, text)

        # Get all the entities in the text and replace them with a marker
        # The text might contain undefined entities that BeautifulSoup
        # will strip out.
        entities = {
            _[0]
            for _ in re.findall(
                r"(&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});)", text, re.IGNORECASE
            )
        }
        for entity in entities:
            marker = str(uuid4())
            self._entity_mapping[entity] = marker
            text = text.replace(entity, marker)
        return "\n".join(
            line if line.strip() else self._newlines_marker
            for line in text.splitlines()
        ).replace("&", self._ampersand_marker)

    def get_soup(self, text):
        """Tries to get the soup from the given test

        If the text is not some xml like think a dummy element will be used to wrap it.
        """
        original_soup = BeautifulSoup(text, self.parser)
        try:
            first_el = next(original_soup.children)
        except StopIteration:
            first_el = None
        if isinstance(first_el, (Doctype, ProcessingInstruction)):
            return original_soup

        markup = "<{null}>{text}</{null}>".format(
            null=self.pretty_element.null_tag_name, text=text
        )
        wrapped_soup = BeautifulSoup(markup, self.parser)
        return getattr(wrapped_soup, self.pretty_element.null_tag_name)

    def pretty_print(self, el):
        """Pretty print an element indenting it based on level"""
        prettified = (
            el().replace(self._newlines_marker, "").replace(self._ampersand_marker, "&")
        )
        # Restore CDATAs
        for cdata in self._cdatas:
            prettified = prettified.replace(
                self._cdata_marker, f"<![CDATA[{cdata}]]>", 1
            )
        # Restore DocTypes
        if self._doctype:
            prettified = prettified.replace(self._doctype_marker, self._doctype)
        # Restore entities
        for entity, marker in self._entity_mapping.items():
            prettified = prettified.replace(marker, entity)
        if self._end_with_newline and not prettified.endswith("\n"):
            prettified += "\n"
        return prettified

    def check(self):
        """Checks if the input object should be prettified"""
        return self.original_text == self()

    def __call__(self):
        if not self.root.getchildren():
            # The parsed content is not even something that looks like an XML
            return self.original_text
        return self.pretty_print(self.root)
