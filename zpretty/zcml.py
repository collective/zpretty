# coding=utf-8
from logging import getLogger
from zpretty.xml import XMLAttributes
from zpretty.xml import XMLElement
from zpretty.xml import XMLPrettifier


logger = getLogger(__name__)


class ZCMLAttributes(XMLAttributes):
    """ Customized attribute formatter for zcml
    """

    _multiline_attributes = ("for",)
    _xml_attribute_order = (
        "name",
        "title",
        "description",
        "package",
        "file",
        "provides",
        "for",
        "factory",
        "manager",
        "permission",
        "class",
        "allowed_attributes",
        "attribute",
        "template",
        "layer",
    )


class ZCMLElement(XMLElement):
    first_attribute_on_new_line = True
    before_closing_multiline = u"    "
    attribute_klass = ZCMLAttributes

    def render_text(self):
        """ Add an empty line between each element
        """
        return super(ZCMLElement, self).render_text()


class ZCMLPrettifier(XMLPrettifier):
    """ Prettify according to the ZCML style guide
    """

    pretty_element = ZCMLElement
