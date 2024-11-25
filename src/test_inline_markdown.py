import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, TextType


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
        node = TextNode("This **is** a test!", TextType.TEXT)
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


class TestMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        node = extract_markdown_images("![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected_output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(node, expected_output)

    def test_multiple_images(self):
        node = extract_markdown_images(
            """This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) 
            and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"""
        )
        expected_output = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(node, expected_output)

    def test_no_alt_text_images(self):
        with self.assertRaises(ValueError):
            node = extract_markdown_images("![](https://i.imgur.com/aKaOqIh.gif)")


class TestMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        node = extract_markdown_links("[to boot dev](https://www.boot.dev)")
        expected_output = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(node, expected_output)

    def test_multiple_links(self):
        node = extract_markdown_links(
            """This is text with a link [to boot dev](https://www.boot.dev)
            and [to youtube](https://www.youtube.com/@bootdotdev)"""
        )
        expected_output = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(node, expected_output)

    def test_no_alt_text_links(self):
        with self.assertRaises(ValueError):
            node = extract_markdown_links("[](https://www.boot.dev)")


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 1
        assert nodes[0].text == "Just plain text"

        # Test 2: One image
        node = TextNode("Hello ![test](test.png) world", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 3
        assert nodes[0].text == "Hello "
        assert nodes[1].text == "test"
        assert nodes[1].text_type == TextType.IMAGE
        assert nodes[1].url == "test.png"

    def test_split_nodes_link(self):
        # Test 1: No links
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 1
        assert nodes[0].text == "Just plain text"

        # Test 2: One link
        node = TextNode("Hello [test](https://google.com) world", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 3
        assert nodes[0].text == "Hello "
        assert nodes[1].text == "test"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://google.com"


class TestTextToTextNodes(unittest.TestCase):
    def test_multiple_nodes(self):
        test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        actual = text_to_textnodes(test_text)

        self.assertEqual(len(actual), len(expected))
        for i, _ in enumerate(actual):
            self.assertEqual(actual[i].text, expected[i].text)
            self.assertEqual(actual[i].text_type, expected[i].text_type)
            self.assertEqual(actual[i].url, expected[i].url)

    def test_multiple_bold_instances(self):
        test_text = "**bold** some text **more bold**"
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" some text ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        actual = text_to_textnodes(test_text)

        self.assertEqual(len(actual), len(expected))

    def test_incomplete_bold_delimiter(self):
        test_text = "**bold without closing and **another bold**"
        with self.assertRaises(ValueError):
            text_to_textnodes(test_text)


if __name__ == "__main__":
    unittest.main()