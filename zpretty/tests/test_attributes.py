from bs4 import BeautifulSoup
from unittest import TestCase
from zpretty.attributes import PrettyAttributes
from zpretty.elements import PrettyElement


class FakeConfig:
    split_class = False


class TestZPrettyAttributess(TestCase):
    """Test zpretty"""

    def get_element(self, text, level=0):
        """Given a text return a PrettyElement"""
        soup = BeautifulSoup(
            "<soup><fake_root>%s</fake_root></soup>" % text, "html.parser"
        )
        return PrettyElement(FakeConfig(), soup.fake_root.next_element, level)

    def assertPrettifiedAttributes(self, attributes, expected, level=0, config=None):
        """Check if the attributes are properly sorted and formatted"""
        if level == 0:
            el = None
        else:
            el = self.get_element("a", level)

        config = config if config else FakeConfig()

        pretty_attribute = PrettyAttributes(config, attributes, el)
        observed = pretty_attribute()
        self.assertEqual(observed, expected)

    def test_no_attributes(self):
        self.assertPrettifiedAttributes({}, "")
        self.assertPrettifiedAttributes({}, "", level=2)

    def test_one_attribute(self):
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"')
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"', level=1)
        self.assertPrettifiedAttributes({"a": "1"}, 'a="1"', level=2)

    def test_value_with_double_quoptes(self):
        self.assertPrettifiedAttributes({"a": '"'}, "a='\"'")

    def test_transform_forbidden_characters(self):
        self.assertPrettifiedAttributes({"a": "> < &"}, 'a="&gt; &lt; &amp;"')

    def test_many_attributes_attribute(self):
        self.assertPrettifiedAttributes({"a": "1", "b": "2"}, 'a="1"\nb="2"')
        self.assertPrettifiedAttributes(
            {"a": "1", "b": "2"}, '    a="1"\n    b="2"', level=1
        )
        self.assertPrettifiedAttributes(
            {"a": "1", "b": "2"}, '      a="1"\n      b="2"', level=2
        )

    def test_tal_define(self):
        self.assertPrettifiedAttributes(
            {"tal:define": "a 1; b 2"},
            "\n".join(('tal:define="', "  a 1;", "  b 2;", '"')),
        )

    def test_format_attributes_many_attribute(self):
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

    def test_class_multiline_no_split(self):
        """Class attributes with multiple values should be split."""
        self.assertPrettifiedAttributes(
            {"class": "class1 class2 ${python: 'class3' if True else ''} class4"},
            '''class="class1 class2 ${python: 'class3' if True else ''} class4"''',
        )

    def test_class_multiline(self):
        """Class attributes with multiple values should be split."""
        config = FakeConfig()
        config.split_class = True
        self.assertPrettifiedAttributes(
            {"class": "class1 class2 ${python: 'class3' if True else ''} class4"},
            "\n".join(
                (
                    'class="',
                    "  class1",
                    "  class2",
                    "  ${python: 'class3' if True else ''}",
                    "  class4",
                    '"',
                )
            ),
            0,
            config,
        )

    def test_data_pat_singleline(self):
        """Class with single values should not be split."""
        config = FakeConfig()
        config.split_class = True
        self.assertPrettifiedAttributes(
            {"class": "class1"}, 'class="class1"', 0, config
        )

    def test_data_pat_empty(self):
        """Empty class attributes should not be split."""
        config = FakeConfig()
        config.split_class = True
        self.assertPrettifiedAttributes({"class": ""}, 'class=""', 0, config)
