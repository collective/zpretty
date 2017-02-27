# coding=utf-8
from bs4.builder._lxml import LXMLTreeBuilderForXML
from logging import getLogger
from lxml import etree
from zpretty.attributes import PrettyAttributes
from zpretty.elements import PrettyElement
from zpretty.prettifier import ZPrettifier


logger = getLogger(__name__)


class ZCMLAttributes(PrettyAttributes):
    ''' Customized attribute formatter for zcml
    '''
    _multiline_attributes = (
        'for',
    )
    _zcml_attribute_order = (
        'name',
        'title',
        'description',
        'package',
        'file',
        'provides',
        'for',
        'factory',
        'manager',
        'permission',
        'class',
        'allowed_attributes',
        'attribute',
        'template',
        'layer',
    )

    def sort_attributes(self, name):
        '''Sort ZCML attributes in a consistent way
        '''
        if name in self._zcml_attribute_order:
            return (100 + self._zcml_attribute_order.index(name))
        return super(ZCMLAttributes, self).sort_attributes(name)


class ZCMLElement(PrettyElement):
    first_attribute_on_new_line = True
    before_closing_multiline = u'    '
    attribute_klass = ZCMLAttributes

    def is_self_closing(self):
        ''' Is this element self closing?
        '''
        if not self.is_tag():
            raise ValueError('This is not a tag')
        # Just check if the element has some content.
        return not self.getchildren()

    @property
    def tag(self):
        ''' Return the tag name
        '''
        if not self.context.prefix:
            return self.context.name
        else:
            return u':'.join((
                self.context.prefix,
                self.context.name,
            ))

    def render_text(self):
        ''' Add an empty line between each element
        '''
        return super(ZCMLElement, self).render_text()


class ZCMLTreeBuilder(LXMLTreeBuilderForXML):
    ''' Override the default Tree builder
    '''
    def default_parser(self, encoding):
        # This can either return a parser object or a class, which
        # will be instantiated with default arguments.
        if self._default_parser is not None:
            return self._default_parser
        return etree.XMLParser(
            target=self,
            strip_cdata=False,
            recover=True,
            encoding=encoding,
            remove_blank_text=False,
            attribute_defaults=False,
            dtd_validation=False,
            load_dtd=False,
            no_network=True,
            ns_clean=True,
            resolve_entities=False,
            remove_comments=False,
            remove_pis=False,
            collect_ids=False,
            compact=False,
        )


class ZCMLPrettifier(ZPrettifier):
    ''' Prettify according to the ZCML style guide
    '''
    parser = 'xml'
    pretty_element = ZCMLElement
    builder = ZCMLTreeBuilder()
