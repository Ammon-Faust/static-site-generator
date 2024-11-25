import re
from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):  # Enum of text types we will take
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:  # Defining TextNode
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):  # Takes text node and turns it into a LeafNode
    if text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(text_node.text, "b", None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(text_node.text, "i", None)
    if text_node.text_type == TextType.CODE:
        return LeafNode(text_node.text, "code", None)
    if text_node.text_type == TextType.LINK:
        return LeafNode(text_node.text, "a", props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("", "img", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError("Invalid TextType")


