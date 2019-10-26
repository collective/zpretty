# coding=utf-8
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
from bs4.element import Comment
from bs4.element import Doctype
from bs4.element import NavigableString
from bs4.element import ProcessingInstruction
from bs4.element import Tag
from zpretty.attributes import PrettyAttributes
from zpretty.text import endswith_whitespace
from zpretty.text import lstrip_first_line
from zpretty.text import rstrip_last_line
from zpretty.text import startswith_whitespace


class OpenTagException(Exception):
    """ We want this element to be closed
    """

    def __init__(self, el):
        """ el is a PrettyElement instance
        """
        self.el = el

    def __str__(self):
        return "Known self closing tag %r is not closed" % self.el.context


def memo(f):
    """ Simple memoize
    """
    key = "__zpretty_memo__" + f.__name__

    def wrapped(obj):
        if not hasattr(obj, key):
            setattr(obj, key, f(obj))
        return getattr(obj, key)

    return wrapped


class PrettyElement(object):
    """ A pretty element class that can render prettified html
    """

    null_tag_name = u"null_tag_name"

    knownself_closing_elements = [
        "area",
        "base",
        "basefont",
        "br",
        "col",
        "frame",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
    ]
    indent = u"  "
    attribute_klass = PrettyAttributes

    first_attribute_on_new_line = False
    before_closing_multiline = u""

    self_closing_singleline_template = u"{prefix}<{tag}{attributes}/>"
    self_closing_multiline_template = u"\n".join(
        (u"{prefix}<{tag}{attributes}", u"{prefix}{before_closing_multiline}/>")
    )
    start_tag_singleline_template = u"{prefix}<{tag}{attributes}>"
    start_tag_multiline_template = u"\n".join(
        (u"{prefix}<{tag}{attributes}", u"{prefix}{before_closing_multiline}>")
    )
    escaper = EntitySubstitution()

    def __init__(self, context, level=0):
        """ Take something a (bs4) element and an indentation level
        """
        self.context = context
        self.level = level

    def __str__(self):
        """ Reuse the context method
        """
        return str(self.context)

    def __repr__(self):
        """ Try to make evident:

        - the element type
        - the level
        """
        if self.is_comment():
            tag = "!--"
        if self.is_text():
            tag = '""'
        else:
            tag = self.tag
        return "<pretty:{level}:{tag} />".format(tag=tag, level=self.level)

    def is_comment(self):
        """ Check if this element is a comment
        """
        return isinstance(self.context, Comment)

    def is_doctype(self):
        """ Check if this element is a doctype
        """
        return isinstance(self.context, Doctype)

    def is_text(self):
        """ Check if this element is a text

        Also comments and processing instructions
        are instances of NavigableString,
        so we have to make additional checks
        """
        if not isinstance(self.context, NavigableString):
            return False
        if self.is_comment() or self.is_doctype() or self.is_processing_instruction():
            return False
        return True

    def is_tag(self):
        """ Check if this element is a notmal tag
        """
        return isinstance(self.context, Tag)

    def is_self_closing(self):
        """ Is this element self closing?
        """
        if not self.is_tag():
            raise ValueError("This is not a tag")
        # First check if element has some content.
        # If it has it cannot be self closing
        tag_name = self.tag
        if self.getchildren():
            if tag_name in self.knownself_closing_elements:
                raise OpenTagException(self)
            return False
        # Then we have some know elements that we want to be self closing
        if tag_name in self.knownself_closing_elements:
            return True
        # Also elements in the tal namespace may be prettified as self closing
        # if needed, e.g.: <tal:name replace="${here/title}" />
        if tag_name.startswith("tal:"):
            return True
        if tag_name.startswith("metal:"):
            return True
        # All the other elements will have an open an close tag
        return False

    def is_null(self):
        """ We define a special tag null_tag_name to wrap text
        """
        return self.context.name == self.null_tag_name

    def is_processing_instruction(self):
        """ Check if this element is a processing instruction like <?xml...>
        """
        return isinstance(self.context, ProcessingInstruction)

    @memo
    def getparent(self):
        """ Return the element parent as an instance of this class
        """
        parent = self.context.parent
        if not parent or parent.name == BeautifulSoup.ROOT_TAG_NAME:
            return None
        return self.__class__(parent)

    @memo
    def getchildren(self):
        """ Return this element children as instances of this class
        """
        children = []
        next_level = self.level + 1
        for child in getattr(self.context, "children", []):
            child = self.__class__(child, next_level)
            try:
                child.is_tag() and child.is_self_closing()
            except OpenTagException:
                # Fix open tags and repeat
                nephews = reversed(tuple(child.context.children))
                for nephew in nephews:
                    child.context.insert_after(nephew)
                return self.getchildren()
            children.append(child)
        return children

    @property
    def tag(self):
        """ Return the tag name
        """
        return self.context.name

    @property
    def text(self):
        """ Return the text contained in this element (if any)

        Convert the text characters to html entities
        """
        if not isinstance(self.context, NavigableString):
            return u""
        if self.is_comment():
            return self.context
        return self.escaper.substitute_html(self.context.string)

    @property
    @memo
    def attributes(self):
        """ Return the wrapped attributes
        """
        attributes = getattr(self.context, "attrs", {})
        return self.attribute_klass(attributes, self)

    @memo
    def render_content(self):
        """ Render a properly indented the contents of this element
        """
        parts = []
        previous_part = ""
        for idx, child in enumerate(self.getchildren()):
            part = child()
            if child.is_text():
                part = lstrip_first_line(part)
            elif not endswith_whitespace(previous_part):
                part = lstrip_first_line(part)
            else:
                parts[-1] = rstrip_last_line(parts[-1])
            parts.append(part)
            previous_part = child()
        content = u"".join(parts)

        if endswith_whitespace(content):
            content = rstrip_last_line(content)
        return content

    def render_comment(self):
        """ Render a properly indented comment
        """
        prefix = self.indent * self.level
        return u"{prefix}<!--{text}-->".format(prefix=prefix, text=self.text)

    def render_doctype(self):
        """ Render a properly indented comment
        """
        prefix = self.indent * self.level
        return u"{prefix}<!DOCTYPE {text}>".format(prefix=prefix, text=self.text)

    def render_processing_instruction(self):
        """ Render a properly indented processing instruction
        """
        prefix = self.indent * self.level
        return u"{prefix}<?{text}?>".format(prefix=prefix, text=self.text)

    def render_text(self):
        """ Render a properly indented text

        If the text starts with spaces, strip them and add a newline.
        If the text end with spaces, strip them.
        """
        text = self.text
        lines = text.split(u"\n")
        if not lines:
            return u""

        prefix = self.indent * (self.level)
        if len(lines) == 1:
            line = lines[0]
            if not line.strip():
                return u"\n"
            if startswith_whitespace(line):
                line = u"\n" + prefix + "%s" % line.lstrip()
            if endswith_whitespace(line):
                line = line.rstrip() + u"\n"
            return line

        if not lines[0].strip():
            rendered_lines = [u"\n"]
        elif startswith_whitespace(lines[0]):
            rendered_lines = [u"\n" + prefix + "%s\n" % lines[0].rstrip()]
        else:
            rendered_lines = [u"%s\n" % lines[0]]

        for line in lines[1:-1]:
            if not line.strip():
                rendered_lines.append(u"\n")
            else:
                rendered_lines.append(u"%s\n" % line.rstrip())

        if lines[-1].strip():
            rendered_lines.append(u"%s\n" % lines[-1].rstrip())
        else:
            rendered_lines.append(u"")

        text = u"".join(rendered_lines)
        return text

    def attributes_prefix(self):
        """ Return the prefix for the attributes
        """
        if self.first_attribute_on_new_line:
            return u" " * 4
        else:
            return u" " * (len(self.tag) + 2)

    def indent_multiline_attributes(self, attributes):
        """ Indent the attributes to be rendered in a multiline tag
        """
        prefix = self.indent * self.level
        attribute_line_joiner = u"\n" + prefix + self.attributes_prefix()
        attributes = attribute_line_joiner.join(attributes.splitlines())
        if self.first_attribute_on_new_line:
            # prepend a new line and the appropriate space
            attributes = attribute_line_joiner + attributes
        else:
            attributes = u" " + attributes
        return attributes

    def render_self_closing(self):
        """ Render a properly indented a self closing tag
        """
        attributes = self.attributes()
        multiline_attributes = "\n" in attributes
        if multiline_attributes:
            attributes = self.indent_multiline_attributes(attributes)
            template = self.self_closing_multiline_template
        else:
            if attributes:
                # we need a space to separate the tag end
                attributes = u" " + attributes + u" "
            else:
                attributes = u" "
            template = self.self_closing_singleline_template

        prefix = self.indent * self.level
        return template.format(
            attributes=attributes,
            before_closing_multiline=self.before_closing_multiline,
            prefix=prefix,
            tag=self.tag,
        )

    def render_not_self_closing(self):
        """ Render a properly indented not self closing tag
        """
        attributes = self.attributes()
        attributes = self.attributes()
        multiline_attributes = "\n" in attributes
        if multiline_attributes:
            attributes = self.indent_multiline_attributes(attributes)
            open_tag_template = self.start_tag_multiline_template
        else:
            if attributes:
                # we need a space after separate from the tag
                attributes = u" " + attributes
            open_tag_template = self.start_tag_singleline_template

        prefix = self.indent * self.level

        text = self.text and self.render_text() or self.render_content()

        if endswith_whitespace(text):
            if text[-1] != u"\n":
                text = rstrip_last_line(text) + u"\n"
            close_tag_template = u"{prefix}</{tag}>"
        else:
            close_tag_template = u"</{tag}>"

        open_tag = open_tag_template.format(
            before_closing_multiline=self.before_closing_multiline,
            attributes=attributes,
            prefix=prefix,
            tag=self.tag,
        )
        close_tag = close_tag_template.format(prefix=prefix, tag=self.tag)
        return u"{open_tag}{text}{close_tag}".format(
            close_tag=close_tag, open_tag=open_tag, text=text
        )

    @memo
    def __call__(self):
        """ Render the element and its contents properly indented
        """
        if self.is_null():
            return self.render_content()

        if self.is_comment():
            return self.render_comment()

        if self.is_tag():
            if self.is_self_closing():
                return self.render_self_closing()
            else:
                return self.render_not_self_closing()

        if self.is_processing_instruction():
            return self.render_processing_instruction()

        if self.is_doctype():
            return self.render_doctype()

        return self.render_text()
