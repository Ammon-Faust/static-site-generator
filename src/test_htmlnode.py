import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
