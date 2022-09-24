from bs4 import BeautifulSoup
from bs4.element import Doctype
from bs4.element import ProcessingInstruction
from logging import getLogger
from uuid import uuid4
from zpretty.elements import PrettyElement

import fileinput


logger = getLogger(__name__)


class ZPrettifier(object):
    """Wraps and renders some text that may contain xml like stuff"""

    pretty_element = PrettyElement
    parser = "html.parser"
    builder = None
    _end_with_newline = True
    _newlines_marker = str(uuid4())
    _ampersand_marker = str(uuid4())

    def __init__(self, filename="", text="", encoding="utf8"):
        """Create a prettifier instance taking the contents
        from a text or a filename
        """
        self.encoding = encoding
        self.filename = filename
        if self.filename:
            text = "".join(fileinput.input([filename]))
        if not isinstance(text, str):
            text = text.decode(self.encoding)
        self.original_text = text
        self.text = "\n".join(
            line if line.strip() else self._newlines_marker
            for line in text.splitlines()
        ).replace("&", self._ampersand_marker)
        self.soup = self.get_soup(self.text)

        # Cleanup all spurious self._newlines_marker attributes, see #35
        for el in self.soup.find_all(attrs={self._newlines_marker: ""}):
            el.attrs.pop(self._newlines_marker, None)

        self.root = self.pretty_element(self.soup, -1)

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
        if self._end_with_newline and not prettified.endswith("\n"):
            prettified += "\n"
        return prettified

    def check(self):
        """Checks if the input object should be prettified"""
        return self.original_text == self()

    def __call__(self):
        return self.pretty_print(self.root)
