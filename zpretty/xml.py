# coding=utf-8
from bs4.builder._lxml import LXMLTreeBuilderForXML
from logging import getLogger
from lxml import etree
from zpretty.attributes import PrettyAttributes
from zpretty.elements import PrettyElement
from zpretty.prettifier import ZPrettifier


logger = getLogger(__name__)


class XMLAttributes(PrettyAttributes):
    """ Customized attribute formatter for zcml
    """

    _valueless_attributes_are_allowed = False
    _known_valueless_attributes = ()
    _multiline_attributes = ()
    _xml_attribute_order = ()

    def sort_attributes(self, name):
        """Sort ZCML attributes in a consistent way
        """
        if name in self._xml_attribute_order:
            return (100 + self._xml_attribute_order.index(name), name)
        return super(XMLAttributes, self).sort_attributes(name)


class XMLElement(PrettyElement):
    attribute_klass = XMLAttributes

    def is_self_closing(self):
        """ Is this element self closing?
        """
        if not self.is_tag():
            raise ValueError("This is not a tag")
        # Just check if the element has some content.
        return not self.getchildren()

    @property
    def tag(self):
        """ Return the tag name
        """
        if not self.context.prefix:
            return self.context.name
        else:
            return u":".join((self.context.prefix, self.context.name))

    def render_text(self):
        """ Add an empty line between each element
        """
        return super(XMLElement, self).render_text()


class XMLTreeBuilder(LXMLTreeBuilderForXML):
    """ Override the default Tree builder
    """

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


class XMLPrettifier(ZPrettifier):
    """ Prettify according to the ZCML style guide
    """

    parser = "xml"
    pretty_element = XMLElement
    builder = XMLTreeBuilder()
