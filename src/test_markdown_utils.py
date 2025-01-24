import unittest

from markdown_utils import markdown_to_blocks, block_to_block_type


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

    
    def test_block_to_block_type(self):
        type_heading = "heading"
        type_code = "code"
        type_quote = "quote"
        type_unordered_list = "unordered_list"
        type_ordered_list = "ordered_list"
        type_paragraph = "paragraph"

        cases = [
            ("# This is a heading", type_heading),
            ("### This one is also a heading", type_heading),
            ("```\nthis = 'code_block'\na = 3\nb = 10\n```", type_code),
            ("> This is a quote line\n> another quote line", type_quote),
            ("* unordered\n* list\n* testing", type_unordered_list),
            ("- unordered\n- list\n- testing", type_unordered_list),
            ("1. ordered\n2. list\n3. testing", type_ordered_list),
            ("this is just a paragraph", type_paragraph),
            ("> This is not a quote line\nanother not quote line", type_paragraph),
            ("* unordered\nlist\n* testing", type_paragraph),
            ("1. not ordered\nlist\ntesting", type_paragraph),
        ]

        for case in cases:
            block_type = block_to_block_type(case[0])
            
            self.assertEqual(block_type, case[1])


if __name__ == "__main__":
    unittest.main()