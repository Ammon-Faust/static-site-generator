import unittest

from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_multiple_blocks(self):
        test_text = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item
        """

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item""",
        ]

        actual = markdown_to_blocks(test_text)
        self.assertEqual(len(actual), len(expected))

    def test_multiple_empty_lines(self):
        test_text = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.


            * This is the first list item in a list block
            * This is a list item
            * This is another list item
            

        """

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item""",
        ]

        actual = markdown_to_blocks(test_text)
        self.assertEqual(len(actual), len(expected))


if __name__ == "__main__":
    unittest.main()
