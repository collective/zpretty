# coding=utf-8
from bs4 import BeautifulSoup
from logging import getLogger
from zpretty.elements import PrettyElement


logger = getLogger(__name__)


class ZPrettifier(object):
    ''' Wraps and renders some text that may contain xml like stuff
    '''

    encoding = 'utf8'
    pretty_element = PrettyElement

    def __init__(
        self,
        filename='',
        text='',
    ):
        ''' Create a prettifier instance taking the contents
        from a text or a filename
        '''
        self.filename = filename
        if self.filename:
            text = open(self.filename).read()
        if not isinstance(text, unicode):
            text = text.decode(self.encoding)
        self.text = text
        self.soup = self.get_soup(self.text)
        self.root = self.pretty_element(self.soup, -1)

    def get_soup(self, text):
        ''' Tries to get the soup from the given test

        At first it will try to parse the text:

        1. as an xml
        2. as an html
        3. will just return the unparsed text
        '''
        markup = u'<{null}>{text}</{null}>'.format(
            null=self.pretty_element.null_tag_name,
            text=text,
        )
        wrapped_soup = BeautifulSoup(markup, 'html.parser')
        return getattr(wrapped_soup, self.pretty_element.null_tag_name)

    def autofix(self):
        ''' Do various autofx on the soup
        '''

    def pretty_print(self, el):
        ''' Pretty print an element indenting it based on level
        '''
        return el()

    def __call__(self):
        self.autofix()
        return self.pretty_print(self.root)
