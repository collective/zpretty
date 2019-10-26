# coding=utf-8
from bs4 import BeautifulSoup
from logging import getLogger
from uuid import uuid4
from zpretty.elements import PrettyElement

import fileinput


logger = getLogger(__name__)


class ZPrettifier(object):
    """ Wraps and renders some text that may contain xml like stuff
    """

    pretty_element = PrettyElement
    parser = "html.parser"
    builder = None
    _end_with_newline = True
    _newlines_marker = str(uuid4())

    def __init__(self, filename="", text="", encoding="utf8"):
        """ Create a prettifier instance taking the contents
        from a text or a filename
        """
        self.encoding = encoding
        self.filename = filename
        if self.filename:
            text = "".join(fileinput.input([filename]))
        if not isinstance(text, str):
            text = text.decode(self.encoding)
        self.text = "\n".join(
            line if line.strip() else self._newlines_marker
            for line in text.splitlines()
        )
        self.soup = self.get_soup(self.text)
        self.root = self.pretty_element(self.soup, -1)

    def get_soup(self, text):
        """ Tries to get the soup from the given test

        At first it will try to parse the text:

        1. as an xml
        2. as an html
        3. will just return the unparsed text
        """
        markup = u"<{null}>{text}</{null}>".format(
            null=self.pretty_element.null_tag_name, text=text
        )
        wrapped_soup = BeautifulSoup(markup, self.parser, builder=self.builder)
        return getattr(wrapped_soup, self.pretty_element.null_tag_name)

    def autofix(self):
        """ Do various autofx on the soup
        """

    def pretty_print(self, el):
        """ Pretty print an element indenting it based on level
        """
        prettified = el().replace(self._newlines_marker, u"")
        if self._end_with_newline and not prettified.endswith(u"\n"):
            prettified += u"\n"
        return prettified

    def __call__(self):
        self.autofix()
        return self.pretty_print(self.root)
