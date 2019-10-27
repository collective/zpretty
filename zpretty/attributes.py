# coding=utf-8
from logging import getLogger


try:
    from html import escape
except ImportError:
    # Python < 3.8
    from cgi import escape


logger = getLogger(__name__)


class PrettyAttributes(object):
    """ Render attributes in a pretty way.

    - one per line
    - sorted semantically and alphabetically
    - with properly indented and escaped values
    """

    _attribute_template = u'%s="%s"'
    _valueless_attributes_are_allowed = True
    _known_valueless_attributes = ("hidden", "required")
    _multiline_prefix = u"  "
    _multiline_attributes = ()
    _tal_multiline_attributes = (
        u"attributes",
        u"define",
        u"tal:attributes",
        u"tal:define",
    )

    _tal_attribute_order = (
        "tal:define",
        "tal:switch",
        "tal:condition",
        "tal:repeat",
        "tal:case",
        "tal:content",
        "tal:replace",
        "tal:omit-tag",
        "tal:attributes",
        "tal:on-error",
    )

    _i18n_attributes = (
        "i18n:translate",
        "i18n:domain",
        "i18n:context",
        "i18n:source",
        "i18n:target",
        "i18n:name",
        "i18n:attributes",
        "i18n:data",
        "i18n:comment",
        "i18n:ignore",
        "i18n:ignore-attributes",
    )

    def __init__(self, attributes, element=None):
        """ attributes is a dict like object
        """
        self.attributes = attributes
        self.element = element

    def sort_attributes(self, name):
        """This sorts the attribute trying to group them semantically

        Starting from the top:

        1. xml namespaces
        2. class, id
        3. attributes not belonging in to other categories (default)
        4. data- attributes
        5. tal attributes
        6. i18n attributes
        """
        if name.startswith("xmlns"):
            return (0, name)
        if name in ("class", "id"):
            return (100, name)
        if name.startswith("data"):
            return (300, name)
        if "tal:" + name in self._tal_attribute_order:
            tal_index = self._tal_attribute_order.index("tal:" + name)
            return (400 + tal_index, name)
        if name in self._tal_attribute_order:
            tal_index = self._tal_attribute_order.index(name)
            return (400 + tal_index, name)
        if name in self._i18n_attributes:
            return (900, name)
        return (200, name)

    def format_multiline(self, name, value):
        """
        """
        value_lines = filter(None, value.split())
        line_joiner = u"\n" + (u" " * (len(name) + 2))
        return line_joiner.join(value_lines)

    def format_tal_multiline(self, value):
        """ There are some tal specific attributes that contain ; separated
        statements.
        They are used to define variables or set other attributes.
        You can define many variables by adding statements separated by ';'.
        If the statement contains a ';', it will be escaped as ';;'.

        It is convenient to always have those attribute in the form:

        tal:define="
          var1 statement1;
          var2 statement2;
          ...
        "
        """
        # temp skip ';;' the escape sequence to enter a ';' in a statement
        statements = value.replace(";;", "<>").split(";")

        # We always want an empty line first...
        lines = [u""]
        for statement in statements:
            statement = statement.strip()
            if statement:
                if not statement.endswith(";"):
                    statement += u";"
                lines.append(self._multiline_prefix + statement)
        # ... and at the end
        lines.append(u"")

        new_value = u"\n".join(lines)
        # restore ';;'
        return new_value.replace("<>", ";;")

    def can_be_valueless(self, name):
        """ Check if the attribute name can be without a value
        """
        if not self._valueless_attributes_are_allowed:
            return False
        if name.startswith("data-"):
            return True
        if name in self._known_valueless_attributes:
            return True
        return False

    def lines(self):
        """ Take the attributes, sort them and prettify their values
        """
        attributes = self.attributes
        sorted_names = sorted(attributes, key=self.sort_attributes)
        lines = []
        for name in sorted_names:
            value = attributes[name]
            if isinstance(value, list):
                # Happens, e.g., for the class attribute
                value = u" ".join(value)
            if name in self._multiline_attributes:
                value = self.format_multiline(name, value)
            elif name in self._tal_multiline_attributes:
                value = self.format_tal_multiline(value)
            if not value and self.can_be_valueless(name):
                line = name
            else:
                line = self._attribute_template % (name, escape(value))
            lines.append(line)
        return lines

    def __call__(self):
        """ Render the attributes as text
        """
        return u"\n".join(self.lines())
