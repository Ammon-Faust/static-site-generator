import re
from enum import Enum
from warnings import warn

from htmlnode import *


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


def split_nodes_delimiter(
    old_nodes, delimiter, text_type
):  # Splits a list of nodes by a delimiter
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("Missing closing delimiter")
            for i, _ in enumerate(parts):
                if i % 2 == 0:
                    current_type = TextType.TEXT
                    new_nodes.append(TextNode(parts[i], current_type))
                else:
                    current_type = text_type
                    new_nodes.append(TextNode(parts[i], current_type))
    return new_nodes


def extract_markdown_images(text):
    image_texts = re.findall(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
    for alt_text, _ in image_texts:
        if alt_text == "":
            raise ValueError("Missing alt text")
    return image_texts


def extract_markdown_links(text):
    link_texts = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for alt_text, _ in link_texts:
        if alt_text == "":
            raise ValueError("Missing alt text")
    return link_texts


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt_text, url in images:
            parts = current_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            current_text = parts[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt_text, url in links:
            parts = current_text.split(f"[{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            current_text = parts[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes
