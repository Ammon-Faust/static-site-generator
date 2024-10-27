import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    # Test that HTMLNode can be initialized with None values
    def test_None(self):
        node = HTMLNode(None, None, None, None)
    
    # Test that multiple properties are correctly converted to HTML
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'  # Ensure there is a space here
        self.assertEqual(node.props_to_html(), expected_output)

    # Test when no props are passed
    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    # Test single prop being passed
    def test_props_to_html_with_single_prop(self):
        props = {"class": "test-class"}
        node = HTMLNode(props=props)
        expected_output = ' class="test-class"'
        self.assertEqual(node.props_to_html(), expected_output)

class TestLeafNode(unittest.TestCase):
    # Test that a value is required
    def test_empty_value(self):
        node = LeafNode(value=None, tag=None, props=None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Test if an empty tag return raw value
    def test_empty_tag(self):
        node = LeafNode("This is a test!", None, None)
        expected_output = "This is a test!"
        self.assertEqual(node.to_html(), expected_output)
    
    # Test that tags are properly appended
    def test_tag(self):
        node = LeafNode("This is a test!", "p", None)
        expected_output = "<p>This is a test!</p>"
        self.assertEqual(node.to_html(), expected_output)

    # Test if props append correctly
    def test_props(self):
        node = LeafNode("This is a test!", "a", props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = '<a href="https://www.google.com" target="_blank">This is a test!</a>'
        self.assertEqual(node.to_html(), expected_output)

class TestParentNode(unittest.TestCase):
    # Test if an empty list for children is passed
    def test_empty_child(self):
        node = ParentNode("p", [], None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    # Test if there is no child
    def test_no_child(self):
        node = ParentNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()


    # Test for no tag
    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()
    
    # Test for a single child
    def test_single_child(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b"),
            ],
        )
        expected_output = "<p><b>Bold text</b></p>"
        self.assertEqual(node.to_html(), expected_output)


    # Test multple children
    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ],
        )
        expected_output = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_output)
    
    # Test parent prop
    def test_prop(self):
        node = ParentNode(
            "a",
            [
                LeafNode("Bold text", "b"),
            ], props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected_output = '<a href="https://www.google.com" target="_blank"><b>Bold text</b></a>'
        self.assertEqual(node.to_html(), expected_output)
    
    def test_children_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", "a", props={"href": "https://www.google.com", "target": "_blank"}),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", "a", props={"href": "https://www.google.com", "target": "_blank"}),
            ],
        )
        expected_output = '<p><b>Bold text</b><a href="https://www.google.com" target="_blank">Normal text</a><i>italic text</i><a href="https://www.google.com" target="_blank">Normal text</a></p>'
        self.assertEqual(node.to_html(), expected_output)



if __name__ == '__main__':
    unittest.main()
