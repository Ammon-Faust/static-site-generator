import unittest

from htmlnode import *
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type(self):
        node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)

    def test_tags(self):
        node = TextNode("Hello, world!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_text_type(self):
        node = TextNode("**bold**", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(1, len(nodes))
        self.assertEqual("**bold**", nodes[0].text)
        self.assertEqual(TextType.BOLD, nodes[0].text_type)

    def test_missing_delimiter(self):
        node = TextNode("Hello **bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_simple_split(self):
        node =TextNode("This **is** a test!", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(3, len(nodes))
        self.assertEqual("This ", nodes[0].text)
        self.assertEqual(TextType.TEXT, nodes[0].text_type)
        self.assertEqual("is", nodes[1].text)
        self.assertEqual(TextType.BOLD, nodes[1].text_type)
        self.assertEqual(" a test!", nodes[2].text)
        self.assertEqual(TextType.TEXT, nodes[2].text_type)

    def test_multiple_delimiters(self):
        node = TextNode("Hello **bold** world **again**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(5, len(nodes))
        self.assertEqual("Hello ", nodes[0].text)
        self.assertEqual(TextType.TEXT, nodes[0].text_type)
        self.assertEqual("bold", nodes[1].text)
        self.assertEqual(TextType.BOLD, nodes[1].text_type)
        self.assertEqual(" world ", nodes[2].text)
        self.assertEqual(TextType.TEXT, nodes[2].text_type)
        self.assertEqual("again", nodes[3].text)
        self.assertEqual(TextType.BOLD, nodes[3].text_type)
        self.assertEqual("", nodes[4].text)
        self.assertEqual(TextType.TEXT, nodes[4].text_type)

if __name__ == "__main__":
    unittest.main()
