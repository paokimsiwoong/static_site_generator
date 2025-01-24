import unittest

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 해답처럼 markdown_utils.py에서 block 타입들 global로 만든 후 여기서 불러오기
from markdown_utils import (
    markdown_to_blocks, 
    block_to_block_type,
    markdown_to_html_node,
    type_heading,
    type_code,
    type_quote,
    type_unordered_list,
    type_ordered_list,
    type_paragraph,
)


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
    
    def test_markdown_to_html_node(self):
        cases = [
            (
                "# Title\n\n## ul test 1\n\n- ul **first** line\n- ul *second* line\n- ul third line\n\n## ul test 2\n\n* ul first line\n* ul second line\n* ul third line\n\n### ol test\n\n1. ol first line\n2. ol second line\n3. ol third line",
                "<div><h1>Title</h1><h2>ul test 1</h2><ul><li>ul <b>first</b> line</li><li>ul <i>second</i> line</li><li>ul third line</li></ul><h2>ul test 2</h2><ul><li>ul first line</li><li>ul second line</li><li>ul third line</li></ul><h3>ol test</h3><ol><li>ol first line</li><li>ol second line</li><li>ol third line</li></ol></div>"
            ),
            (
                "#### link and image test\n\n> [tbi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)\n> This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)\n> `inline code`\n\n##### code block test\n\n```\nblock = code\ntesting = 0\n```\n\n###### paragraph\n\njust paragraph\nnothing to see here",
                '<div><h4>link and image test</h4><blockquote><a href="https://i.imgur.com/fJRm4Vk.jpeg">tbi wan</a> This is text with a <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img> and <img src="https://i.imgur.com/fJRm4Vk.jpeg" alt="obi wan"></img><br>This is text with a link <a href="https://www.boot.dev">to boot dev</a> and <a href="https://www.youtube.com/@bootdotdev">to youtube</a><br><code>inline code</code></blockquote><h5>code block test</h5><pre><code>block = code<br>testing = 0</code></pre><h6>paragraph</h6><p>just paragraph<br>nothing to see here</p></div>'
            ),
        ]

        for case in cases:
            html_text = markdown_to_html_node(case[0]).to_html()
            # print(html_text)
            # print(case[1])

            # self.assertSequenceEqual(html_text, case[1])

            self.assertEqual(html_text, case[1])


if __name__ == "__main__":
    unittest.main()