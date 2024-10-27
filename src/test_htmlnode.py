import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_None(self):
        node = HTMLNode(None, None, None, None)
    
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'  # Ensure there is a space here
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_with_single_prop(self):
        props = {"class": "test-class"}
        node = HTMLNode(props=props)
        expected_output = ' class="test-class"'
        self.assertEqual(node.props_to_html(), expected_output)

class testLeafNode(unittest.TestCase):
    def test_empty_value(self):
        node = LeafNode(value=None, tag=None, props=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_tag(self):
        node = LeafNode("This is a test!", None, None)
        expected_output = "This is a test!"
        self.assertEqual(node.to_html(), expected_output)
    
    def test_tag(self):
        node = LeafNode("This is a test!", "p", None)
        expected_output = "<p>This is a test!</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_props(self):
        node = LeafNode("This is a test!", "a", props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = '<a href="https://www.google.com" target="_blank">This is a test!</a>'
        self.assertEqual(node.to_html(), expected_output)


if __name__ == '__main__':
    unittest.main()
