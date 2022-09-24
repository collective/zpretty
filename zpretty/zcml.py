from bs4 import BeautifulSoup
from logging import getLogger
from zpretty.xml import XMLAttributes
from zpretty.xml import XMLElement
from zpretty.xml import XMLPrettifier


logger = getLogger(__name__)


class ZCMLAttributes(XMLAttributes):
    """Customized attribute formatter for zcml"""

    # The ZCML guides wants attributes indented by 4 spaces
    prefix = 4 * " "
    _multiline_attributes = ("for",)
    _xml_attribute_order_by_ns_and_tag = {
        "http://namespaces.plone.org/monkey": {
            # https://github.com/plone/collective.monkeypatcher/blob/0acedea2c0599e3d5a2fbe19df7c2431f34f3fff/src/collective/monkeypatcher/meta.py#L72  # noqa: E501
            "patch": (
                "original",
                "replacement",
                "class",
                "module",
                "handler",
                "preservedoc",
                "docstringWarning",
                "description",
                "order",
                "ignoreOriginal",
                "preserveOriginal",
                "preconditions",
            ),
        },
        "http://namespaces.plone.org/plone": {
            # https://github.com/plone/plone.behavior/blob/3f6d9cbf18e4b3994d02a0875f9fcfc2a1c8d1a6/plone/behavior/metaconfigure.py#L110  # noqa: E501
            "behavior": (
                "name",
                "title",
                "description",
                "factory",
                "provides",
                "for",
                "marker",
                "name_only",
                "former_dotted_names",
            ),
            # https://github.com/plone/plone.rest/blob/ca24e17d972174e5043e27b1bc5da5a752cfb924/src/plone/rest/zcml.py#L200  # noqa: E501
            "CORSPolicy": (
                "allow_origin",
                "allow_credentials",
                "allow_methods",
                "expose_headers",
                "allow_headers",
                "max_age",
                "for",
                "layer",
            ),
            # https://github.com/plone/plone.app.portlets/blob/50ee05b7954a2cfa2d1760e14ea712c9d9dfc791/plone/app/portlets/metaconfigure.py#L27  # noqa: E501
            "portlet": (
                "name",
                "interface",
                "assignment",
                "renderer",
                "addview",
                "editview",
                "view_permission",
                "edit_permission",
            ),
            # https://github.com/plone/plone.app.portlets/blob/50ee05b7954a2cfa2d1760e14ea712c9d9dfc791/plone/app/portlets/metaconfigure.py#L120  # noqa: E501
            "portletRenderer": (
                "portlet",
                "class",
                "template",
                "for",
                "layer",
                "view",
                "manager",
            ),
            # https://github.com/plone/plone.contentrules/blob/0b61d5f7b0b4964167e09f0f3f6454e80c5e1efd/plone/contentrules/rule/metaconfigure.py#L26  # noqa: E501
            "ruleAction": (
                "name",
                "title",
                "description",
                "for",
                "event",
                "schema",
                "factory",
                "addview",
                "editview",
            ),
            # https://github.com/plone/plone.contentrules/blob/0b61d5f7b0b4964167e09f0f3f6454e80c5e1efd/plone/contentrules/rule/metaconfigure.py#L7  # noqa: E501
            "ruleCondition": (
                "name",
                "title",
                "description",
                "for",
                "event",
                "schema",
                "factory",
                "addview",
                "editview",
            ),
            # https://github.com/plone/plone.rest/blob/ca24e17d972174e5043e27b1bc5da5a752cfb924/src/plone/rest/zcml.py#L81  # noqa: E501
            "service": (
                "method",
                "accept",
                "factory",
                "for",
                "permission",
                "layer",
                "name",
            ),
            # https://github.com/plone/plone.resource/blob/e0e3048b778b9d3ef90045f49ea11a168c5cf1e4/plone/resource/zcml.py#L37  # noqa: E501
            "static": ("directory", "name", "type"),
            # https://github.com/plone/plone.tiles/blob/93c1474009f54beb4c713f2054445f49dc1a3f1f/plone/tiles/meta.py#L100  # noqa: E501
            "tile": (
                "name",
                "title",
                "description",
                "for",
                "schema",
                "class",
                "template",
                "permission",
                "add_permission",
                "edit_permission",
                "delete_permission",
                "icon",
                "layer",
            ),
        },
        "http://namespaces.zope.org/browser": {
            # https://github.com/zopefoundation/zope.browsermenu/blob/0409ba2f8575a3997b1fec12fc2e0535625b3b65/src/zope/browsermenu/metaconfigure.py#L247  # noqa: E501
            "addMenuItem": (
                "title",
                "description",
                "menu",
                "factory",
                "for",
                "class",
                "view",
                "icon",
                "filter",
                "permission",
                "layer",
                "extra",
                "order",
                "item_class",
            ),
            # https://github.com/zopefoundation/zope.publisher/blob/af5afbb35e490780c0d02d2f6f08f42ade289ebe/src/zope/publisher/zcml.py#L97  # noqa: E501
            "defaultSkin": ("name",),
            # https://github.com/zopefoundation/zope.publisher/blob/af5afbb35e490780c0d02d2f6f08f42ade289ebe/src/zope/publisher/zcml.py#L106  # noqa: E501
            "defaultView": ("name", "for", "layer"),
            # https://github.com/zopefoundation/zope.browserresource/blob/master/src/zope/browserresource/metaconfigure.py#L124  # noqa: E501
            "icon": (
                "name",
                "title",
                "for",
                "file",
                "resource",
                "layer",
                "width",
                "height",
            ),
            # https://github.com/zopefoundation/zope.browserresource/blob/3b82ea3174aa7a6f241f347cbdfe7eebebcff61d/src/zope/browserresource/metaconfigure.py#L174  # noqa: E501
            "i18n-resource": ("name", "defaultLanguage", "permission", "layer"),
            # https://github.com/zopefoundation/z3c.jbot/blob/c16f9302b96b5994939c877a0fcf28d9739ee921/src/z3c/jbot/metaconfigure.py#L56  # noqa: E501
            "jbot": ("directory", "layer"),
            # https://github.com/zopefoundation/zope.browsermenu/blob/0409ba2f8575a3997b1fec12fc2e0535625b3b65/src/zope/browsermenu/metaconfigure.py  # noqa: E501
            "menu": ("id", "title", "description", "class", "interface"),
            # https://github.com/zopefoundation/zope.browsermenu/blob/0409ba2f8575a3997b1fec12fc2e0535625b3b65/src/zope/browsermenu/metaconfigure.py#L109  # noqa: E501
            "menuItem": (
                "menu",
                "title",
                "description",
                "for",
                "action",
                "icon",
                "filter",
                "permission",
                "layer",
                "extra",
                "order",
                "item_class",
            ),
            # https://github.com/zopefoundation/zope.browsermenu/blob/0409ba2f8575a3997b1fec12fc2e0535625b3b65/src/zope/browsermenu/metaconfigure.py#L151  # noqa: E501
            "menuItems": ("menu", "for", "permission", "layer"),
            # https://github.com/zopefoundation/zope.browserpage/blob/52ca649ab013cdc4e7e306efcd30585da9087272/src/zope/browserpage/metaconfigure.py#L109  # noqa: E501
            "page": (
                "name",
                "for",
                "class",
                "allowed_interface",
                "allowed_attributes",
                "attribute",
                "template",
                "permission",
                "layer",
                "menu",
                "title",
            ),
            # https://github.com/zopefoundation/zope.browserpage/blob/52ca649ab013cdc4e7e306efcd30585da9087272/src/zope/browserpage/metaconfigure.py#L181  # noqa: E501
            "pages": (
                "for",
                "class",
                "allowed_interface",
                "allowed_attributes",
                "permission",
                "layer",
            ),
            # https://github.com/zopefoundation/Zope/blob/e3dbd32848e3ea97e2146a9fa690c63555bf61a5/src/Products/Five/fiveconfigure.py#L32  # noqa: E 501
            "pagesFromDirectory": ("directory", "module", "for", "permission", "layer"),
            # https://github.com/zopefoundation/zope.browserresource/blob/3b82ea3174aa7a6f241f347cbdfe7eebebcff61d/src/zope/browserresource/metaconfigure.py#L54  # noqa: E501
            "resource": (
                "name",
                "factory",
                "file",
                "image",
                "template",
                "permission",
                "layer",
            ),
            # https://github.com/zopefoundation/zope.browserresource/blob/3b82ea3174aa7a6f241f347cbdfe7eebebcff61d/src/zope/browserresource/metaconfigure.py#L102  # noqa: E501
            "resourceDirectory": ("name", "directory", "layer", "permission"),
            # https://github.com/zopefoundation/Zope/blob/e3dbd32848e3ea97e2146a9fa690c63555bf61a5/src/Products/Five/sizeconfigure.py  # noqa: E501
            "sizable": ("class",),
            # https://github.com/zopefoundation/z3c.jbot/blob/c16f9302b96b5994939c877a0fcf28d9739ee921/src/z3c/jbot/metaconfigure.py#L56  # noqa: E501
            "templateOverrides": ("directory", "layer"),
            # https://github.com/zopefoundation/zope.browserresource/blob/3b82ea3174aa7a6f241f347cbdfe7eebebcff61d/src/zope/browserresource/metaconfigure.py#L188  # noqa: E501
            "translation": ("language", "file", "image"),
            # https://github.com/zopefoundation/zope.browserpage/blob/52ca649ab013cdc4e7e306efcd30585da9087272/src/zope/browserpage/metaconfigure.py#L210  # noqa: E501
            "view": (
                "name",
                "provides",
                "for",
                "class",
                "allowed_interface",
                "allowed_attributes",
                "permission",
                "layer",
                "menu",
                "title",
            ),
            # https://github.com/zopefoundation/zope.viewlet/blob/d57ed30b35ca3f0d821cbb673513e63ee0747ffa/src/zope/viewlet/metaconfigure.py#L92  # noqa: E501
            "viewlet": (
                "name",
                "for",
                "view",
                "manager",
                "class",
                "allowed_interface",
                "allowed_attributes",
                "attribute",
                "template",
                "permission",
                "layer",
            ),
            # https://github.com/zopefoundation/zope.viewlet/blob/d57ed30b35ca3f0d821cbb673513e63ee0747ffa/src/zope/viewlet/metaconfigure.py#L28  # noqa: E501
            "viewletManager": (
                "name",
                "provides",
                "for",
                "view",
                "class",
                "allowed_interface",
                "allowed_attributes",
                "template",
                "permission",
                "layer",
            ),
        },
        "http://namespaces.zope.org/cache": {
            # https://github.com/zopefoundation/z3c.caching/blob/bd1a6cac1bef90b2d5c3c7cb783ae335feee4dff/src/z3c/caching/zcml.py#L36  # noqa: E501
            "ruleset": ("for", "ruleset"),
            # https://github.com/zopefoundation/z3c.caching/blob/bd1a6cac1bef90b2d5c3c7cb783ae335feee4dff/src/z3c/caching/zcml.py#L23  # noqa: E501
            "rulesetType": ("name", "title", "description"),
        },
        "http://namespaces.zope.org/cmf": {
            # https://github.com/zopefoundation/Products.CMFCore/blob/147efe3192b659211d07997e1923bd7de0c32361/Products/CMFCore/zcml.py#L64  # noqa: E501
            "registerDirectory": ("name", "directory", "recursive", "ignore"),
        },
        "http://namespaces.zope.org/five": {
            # TODO: OFS/meta.zcml
        },
        "http://namespaces.zope.org/ftw.upgrade": {
            # https://github.com/4teamwork/ftw.upgrade/blob/c003c2f5c2ef63eef9efd23cdf754174a66ebabe/ftw/upgrade/directory/zcml.py#L38  # noqa: E501
            "directory": ("profile", "directory", "soft_dependencies"),
            # https://github.com/4teamwork/ftw.upgrade/blob/c003c2f5c2ef63eef9efd23cdf754174a66ebabe/ftw/upgrade/zcml.py#L52  # noqa: E501
            "importProfile": (
                "title",
                "description",
                "profile",
                "source",
                "destination",
                "directory",
                "handler",
            ),
        },
        "http://namespaces.zope.org/genericsetup": {
            # https://github.com/zopefoundation/Products.GenericSetup/blob/c46e0a4f026fc1355f8a3c002f1515d4c8f63715/Products/GenericSetup/zcml.py#L136  # noqa: E501
            "exportStep": ("name", "title", "description", "handler"),
            # https://github.com/zopefoundation/Products.GenericSetup/blob/c46e0a4f026fc1355f8a3c002f1515d4c8f63715/Products/GenericSetup/zcml.py#L183  # noqa: E501
            "importStep": ("name", "title", "description", "handler"),
            # https://github.com/zopefoundation/Products.GenericSetup/blob/c46e0a4f026fc1355f8a3c002f1515d4c8f63715/Products/GenericSetup/zcml.py#L89  # noqa: E501
            "registerProfile": (
                "name",
                "title",
                "description",
                "provides",
                "for",
                "directory",
                "pre_handler",
                "post_handler",
            ),
            # https://github.com/zopefoundation/Products.GenericSetup/blob/c46e0a4f026fc1355f8a3c002f1515d4c8f63715/Products/GenericSetup/zcml.py#L322  # noqa: E501
            "upgradeDepends": (
                "title",
                "description",
                "profile",
                "source",
                "destination",
                "import_profile",
                "import_steps",
                "run_deps",
                "purge",
                "checker",
                "sortkey",
            ),
            # https://github.com/zopefoundation/Products.GenericSetup/blob/c46e0a4f026fc1355f8a3c002f1515d4c8f63715/Products/GenericSetup/zcml.py#L310  # noqa: E501
            "upgradeStep": (
                "title",
                "description",
                "profile",
                "source",
                "destination",
                "handler",
                "checker",
                "sortkey",
            ),
            # https://github.com/zopefoundation/Products.GenericSetup/blob/c46e0a4f026fc1355f8a3c002f1515d4c8f63715/Products/GenericSetup/zcml.py#L343  # noqa: E501
            "upgradeSteps": ("profile", "source", "destination", "sortkey"),
        },
        "http://namespaces.zope.org/i18n": {
            # https://github.com/zopefoundation/zope.i18n/blob/59d212f62d20f9bad168a0dcb8bb137bd625130b/src/zope/i18n/zcml.py#L78  # noqa: E501
            "registerTranslations": ("directory", "domain"),
        },
        "http://namespaces.zope.org/pluggableauthservice": {
            # https://github.com/zopefoundation/Products.PluggableAuthService/blob/f1d7aac8d76ba4840d46fc1e144083bf103d9c9a/Products/PluggableAuthService/zcml.py#L44  # noqa: E501
            "registerMultiPlugin": ("class", "meta_type"),
        },
        "http://namespaces.zope.org/z3c": {
            # https://github.com/zopefoundation/z3c.form/blob/440eb18c541b88f64e88be9b66fbc27748f75af2/src/z3c/form/zcml.py#L133  # noqa: E501
            "objectWidgetTemplate": (
                "for",
                "view",
                "schema",
                "field",
                "widget",
                "template",
                "layer",
            ),
            # https://github.com/zopefoundation/z3c.form/blob/440eb18c541b88f64e88be9b66fbc27748f75af2/src/z3c/form/zcml.py#L114  # noqa: E501
            "widgetLayout": (
                "for",
                "view",
                "field",
                "widget",
                "template",
                "layer",
                "mode",
                "contentType",
            ),
            # https://github.com/zopefoundation/z3c.form/blob/440eb18c541b88f64e88be9b66fbc27748f75af2/src/z3c/form/zcml.py#L96  # noqa: E501
            "widgetTemplate": (
                "for",
                "view",
                "field",
                "widget",
                "template",
                "layer",
                "mode",
                "contentType",
            ),
        },
        "http://namespaces.zope.org/zope": {
            # https://github.com/zopefoundation/zope.component/blob/e7fe69a371afd52781a3c49c130768b607bcff48/src/zope/component/zcml.py#L164  # noqa: E501
            "adapter": (
                "factory",
                "provides",
                "for",
                "name",
                "permission",
                "trusted",
                "locate",
            ),
            # https://github.com/zopefoundation/zope.configuration/blob/022ff7a08af430f9159ffb1574fd908c17745b45/src/zope/configuration/xmlconfig.py#L561  # noqa: E501
            "exclude": ("package", "package", "files"),
            # https://github.com/zopefoundation/zope.configuration/blob/022ff7a08af430f9159ffb1574fd908c17745b45/src/zope/configuration/xmlconfig.py#L524  # noqa: E501
            "include": ("package", "file", "files"),
            # https://github.com/zopefoundation/zope.configuration/blob/022ff7a08af430f9159ffb1574fd908c17745b45/src/zope/configuration/xmlconfig.py#L594  # noqa: E501
            "includeOverrides": ("package", "file", "files"),
            # https://github.com/zopefoundation/zope.component/blob/e7fe69a371afd52781a3c49c130768b607bcff48/src/zope/component/zcml.py#L429  # noqa: E501
            "interface": ("interface", "type", "name"),
            # https://github.com/zopefoundation/AccessControl/blob/458139e987ee79c51438ddb7342300a673222285/src/AccessControl/security.py#L177  # noqa: E501
            "permission": ("id", "title", "description"),
            # https://github.com/zopefoundation/zope.component/blob/e7fe69a371afd52781a3c49c130768b607bcff48/src/zope/component/zcml.py#L616  # noqa: E501
            "resource": (
                "factory",
                "provides",
                "type",
                "name",
                "permission",
                "allowed_interface",
                "allowed_attributes",
            ),
            # https://github.com/zopefoundation/AccessControl/blob/458139e987ee79c51438ddb7342300a673222285/src/AccessControl/security.py#L202  # noqa: E501
            "role": ("name",),
            # https://github.com/zopefoundation/zope.component/blob/e7fe69a371afd52781a3c49c130768b607bcff48/src/zope/component/zcml.py#L295  # noqa: E501
            "subscriber": (
                "factory",
                "provides",
                "for",
                "handler",
                "permission",
                "trusted",
                "locate",
            ),
            # https://github.com/zopefoundation/zope.component/blob/e7fe69a371afd52781a3c49c130768b607bcff48/src/zope/component/zcml.py#L373 # noqa: E501
            "utility": (
                "factory",
                "provides",
                "name",
                "component",
                "permission",
            ),
            # https://github.com/zopefoundation/zope.component/blob/e7fe69a371afd52781a3c49c130768b607bcff48/src/zope/component/zcml.py#L523 # noqa: E501
            "view": (
                "name",
                "factory",
                "allowed_interface",
                "allowed_attributes",
                "provides",
                "for",
                "permission",
                "type",
            ),
        },
    }

    # This will be used when no suitable match is found
    _xml_attribute_order_fallback = (
        "name",
        "title",
        "description",
        "package",
        "file",
        "for",
        "provides",
        "factory",
        "manager",
        "class",
        "allowed_attributes",
        "attribute",
        "template",
        "permission",
        "layer",
    )

    @property
    def _xml_attribute_order(self):
        """Sort the attributes based on the element

        _xml_attribute_order_by_ns_and_tag comments contain references
        to the directives declaration
        The attribute order is inspired by Python code signature of the directives,
        but given it is highly inconsistent some arbitrary decisions have been made.

        In particular:
        - optional element (like layer) are sorted after the others
        - class related attributes in views (i.e. allowed_interfaces)
          are sorted right after the class attribute
        - name, title, description are usually sorted first (except for view
          where the title is sorted after the menu attribute)
        """
        try:
            ns = self.element.context.namespace
            name = self.element.context.name
        except AttributeError:
            ns = ""
            name = ""

        mapping_by_namespace = self._xml_attribute_order_by_ns_and_tag.get(ns, {})
        return mapping_by_namespace.get(name, self._xml_attribute_order_fallback)

    def format_multiline(self, name, value):
        """We have two cases according if we have just one attribute or more

        1. single attribute
          1.1 the the element prefix (if any)
          1.2 as many spaces as the element name
          1.2 as many spaces as the attribute name
          1.3 four spaces spaces (leading `<` and space between element and attribute
              the `="`)

        2. many attributes we need to add:
          2.1 the the element prefix (if any)
          2.2 attribute indentation (4 spaces)
          2.3 as many spaces as the attribute name
          2.4 2 spaces to take into account the leading `="`
        """
        value_lines = filter(None, value.split())
        if len(self) == 1:
            line_joiner = (
                "\n"
                + getattr(self.element, "prefix", "")
                + " " * len(getattr(self.element, "tag", ""))
                + " " * len(name)
                + " " * 4
            )
        else:
            line_joiner = (
                "\n"
                + getattr(self.element, "prefix", "")
                + self.prefix
                + " " * len(name)
                + " " * 2
            )
        return line_joiner.join(value_lines)

    def lstrip(self):
        """Actually we do not want to remove the spaces"""
        return self()

    def __call__(self):
        """Render the attributes as text

        Render and an empty string if no attributes
        If we have one attribute we do not indent it
        If we have many we indent them by 4 spaces + the indentation of the element
        """
        if len(self) == 0:
            return ""
        if len(self) == 1:
            for line in self.lines():
                return line

        if self.element:
            prefix = self.element.prefix + self.prefix
        else:
            prefix = self.prefix

        lines = self.lines()
        return prefix + f"\n{prefix}".join(lines)


class ZCMLElement(XMLElement):
    before_closing_multiline = "    "
    attribute_klass = ZCMLAttributes

    self_closing_multiline_template = "\n".join(
        ("{prefix}<{tag}\n{attributes}", "{prefix}{before_closing_multiline}/>")
    )
    start_tag_multiline_template = "\n".join(
        ("{prefix}<{tag}\n{attributes}", "{prefix}{before_closing_multiline}>")
    )


class ZCMLPrettifier(XMLPrettifier):
    """Prettify according to the ZCML style guide"""

    pretty_element = ZCMLElement

    def get_soup(self, text):
        """Tries to get the soup from the given text"""
        markup = "<{null}>{text}</{null}>".format(
            null=self.pretty_element.null_tag_name, text=text
        )
        wrapped_soup = BeautifulSoup(markup, self.parser)
        return getattr(wrapped_soup, self.pretty_element.null_tag_name)
