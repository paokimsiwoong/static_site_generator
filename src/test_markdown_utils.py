import unittest

from markdown_utils import markdown_to_blocks


class TestMarkdownUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        cases = [
            (
                """
                # This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is the first list item in a list block
                * This is a list item
                * This is another list item
                """,
                (
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
                )
            ),
            (
                """
                # This is a heading



                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is the first list item in a list block
                * This is a list item
                * This is another list item
                * This is another list item
                * This is another list item
                    
                This is a paragraph of text. It has some **bold** and *italic* words inside of it.
                This is a paragraph of text. It has some **bold** and *italic* words inside of it.
                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                """,
                (
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n* This is another list item\n* This is another list item",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                )
            ),
        ]

        for case in cases:
            blocks = markdown_to_blocks(case[0])
            # print(blocks)

            self.assertSequenceEqual(blocks, case[1])


if __name__ == "__main__":
    unittest.main()