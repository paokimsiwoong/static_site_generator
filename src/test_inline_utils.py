import unittest

from textnode import TextNode, TextType
from inline_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineUtils(unittest.TestCase):
    def test_splitter(self):
        cases = [
            (
                ("This is text with a `code block` word", TextType.RAW), 
                (
                    TextNode("This is text with a ", TextType.RAW), 
                    TextNode("code block", TextType.CODE), 
                    TextNode(" word", TextType.RAW),
                )
            ),
            (
                ("*testing* is ongoing **right***now*", TextType.RAW),
                (
                    TextNode("testing", TextType.ITALIC),
                    TextNode(" is ongoing ", TextType.RAW),
                    TextNode("right", TextType.BOLD),
                    TextNode("now", TextType.ITALIC),
                )
            ),
            (
                ("ERROR*ERROR", TextType.RAW),
                (
                    "ERRRRRRRRRR"
                )
            ),
            (
                ("`ERROR`*`ERROR", TextType.RAW),
                (
                    "ERRRRRRRRRR"
                )
            ),
            (
                ("ER**ROR*ERR `OR`", TextType.RAW),
                (
                    "ERRRRRRRRRR"
                )
            ),
            (
                ("This is text with a `` word", TextType.RAW), 
                (
                    TextNode("This is text with a ", TextType.RAW), 
                    TextNode(" word", TextType.RAW),
                )
            ),
        ]

        for case in cases:
            # print(case[0])
            try:
                node = TextNode(*case[0])
                # print(node)
                new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
                new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
                new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
                # print(new_nodes)

                for new_node, expected in zip(new_nodes, case[1]):
                    # print(new_node)
                    # print(expected)
                    self.assertEqual(new_node, expected)
            except Exception as e:
                # print(e)
                with self.assertRaises(ValueError):
                    raise e
                

    def test_extract_images(self):
        cases = [
            (
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
            ),
            (
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                []
            ),
            (
                "![tbi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                [('tbi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'), ('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
            ),
        ]

        for case in cases:
            self.assertEqual(extract_markdown_images(case[0]), case[1])


    def test_extract_links(self):
        cases = [
            (
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                []
            ),
            (
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
            ),
            (
                "[tbi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                [('tbi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
            ),
            (
                "[tbi wan]](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                [('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
            ),
        ]

        for case in cases:
            self.assertEqual(extract_markdown_links(case[0]), case[1])

    def test_split_nodes_image(self):
        cases = [
            (
                "[tbi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", 
                (
                    TextNode("[tbi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ", TextType.RAW), 
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                    TextNode(" and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.RAW),
                )
            ),
            (
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                (
                    TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.RAW),
                )
            ),
            (
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                (
                    TextNode("This is text with a ", TextType.RAW),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", TextType.RAW),
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                )
            )
        ]

        for case in cases:

            node = TextNode(case[0], TextType.RAW)
            # print(node)
            new_nodes = split_nodes_image([node])

            for new_node, expected in zip(new_nodes, case[1]):
                # print(new_node)
                # print(expected)
                self.assertEqual(new_node, expected)


    def test_split_nodes_link(self):
        cases = [
            (
                "[tbi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", 
                (
                    TextNode("tbi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ", TextType.RAW), 
                    TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
                )
            ),
            (
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                (
                    TextNode("This is text with a link ", TextType.RAW),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.RAW),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                )
            ),
            (
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                (
                    TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.RAW),
                )
            )
        ]

        for case in cases:

            node = TextNode(case[0], TextType.RAW)
            # print(node)
            new_nodes = split_nodes_link([node])

            for new_node, expected in zip(new_nodes, case[1]):
                # print(new_node)
                # print(expected)
                self.assertEqual(new_node, expected)


    def test_text_to_textnodes(self):
        cases = [
            (
                "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
                (
                    TextNode("This is ", TextType.RAW),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.RAW),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.RAW),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.RAW),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.RAW),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                )
            ),
        ]

        for case in cases:
            new_nodes = text_to_textnodes(case[0])
            # print(new_nodes)

            for new_node, expected in zip(new_nodes, case[1]):
                # print(new_node)
                # print(expected)
                self.assertEqual(new_node, expected)


if __name__ == "__main__":
    unittest.main()