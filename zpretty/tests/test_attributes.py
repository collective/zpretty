from bs4 import BeautifulSoup
from typing import Dict
from unittest import TestCase
from zpretty.attributes import PrettyAttributes
from zpretty.elements import PrettyElement


class TestZPrettyAttributess(TestCase):
    """Test zpretty"""

    def get_element(self, text: str, level: int = 0) -> PrettyElement:
        """Given a text return a PrettyElement"""
        soup = BeautifulSoup(
            "<soup><fake_root>%s</fake_root></soup>" % text, "html.parser"
        )
        return PrettyElement(soup.fake_root.next_element, level)

    def assertPrettifiedAttributes(
        self, attributes: dict[str, str], expected: str, level: int = 0
    ) -> None:
        """Check if the attributes are properly sorted and formatted"""
        if level == 0:
            el = None
        else:
            el = self.get_element("a", level)
        pretty_attribute = PrettyAttributes(attributes, el)
        observed = pretty_attribute()
        self.assertEqual(observed, expected)

    def test_no_attributes(self) -> None:
        self.assertPrettifiedAttributes({}, "")
        self.assertPrettifiedAttributes({}, "", level=2)

    def test_one_attribute(self) -> None:
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"')
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"', level=1)
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"', level=2)

    def test_value_with_double_quoptes(self) -> None:
        self.assertPrettifiedAttributes({"a": '"'}, "a='\"'")

    def test_transform_forbidden_characters(self) -> None:
        self.assertPrettifiedAttributes({"a": "> < &"}, 'a="&gt; &lt; &amp;"')

    def test_many_attributes_attribute(self) -> None:
        self.assertPrettifiedAttributes({"a": "1", "b": "2"}, 'a="1"\nb="2"')
        self.assertPrettifiedAttributes(
            {"a": "1", "b": "2"}, '    a="1"\n    b="2"', level=1
        )
        self.assertPrettifiedAttributes(
            {"a": "1", "b": "2"}, '      a="1"\n      b="2"', level=2
        )

    def test_tal_define(self) -> None:
        self.assertPrettifiedAttributes(
            {"tal:define": "a 1; b 2"},
            "\n".join(('tal:define="', "  a 1;", "  b 2;", '"')),
        )

    def test_format_attributes_many_attribute(self) -> None:
        self.assertPrettifiedAttributes(
            {
                "a": "1",
                "b": "2",
                "class": "hidden",
                "tal:define": "a 1; b 2",
                "data-multiline": "foo\n   bar",
            },
            "\n".join(
                (
                    'class="hidden"',
                    'a="1"',
                    'b="2"',
                    'data-multiline="foo',
                    '   bar"',
                    'tal:define="',
                    "  a 1;",
                    "  b 2;",
                    '"',
                )
            ),
        )
