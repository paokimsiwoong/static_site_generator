import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Both test functions and file names must start with test_ 
    # to be discoverable by unittest
    # ==> 파일이름 : test_****.py, 함수이름 : def test_****(self):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def test_eq(self):
        # __eq__ 잘 작동하나 확인
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        # self.assertEqual 
        # Fail if the two objects are unequal as determined by the '==' operator.
        # 반대로 self.assertNotEqual은 반대로 작동
        # => 두 입력이 같지 않을 때 테스트 통과

    def test_not_eq(self):
        # __eq__ 잘 작동하나 확인(이번에는 다를 때 제대로 다르다고 판단하는지 확인)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("This is a text node", TextType.BOLD)
        node6 = TextNode("This is a text node", TextType.BOLD, "http://localhost:8888")
        self.assertNotEqual(node5, node6)


class TestSplitNodeDelimiter(unittest.TestCase):
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
                print(new_nodes)

                for new_node, expected in zip(new_nodes, case[1]):
                    # print(new_node)
                    # print(expected)
                    self.assertEqual(new_node, expected)
            except Exception as e:
                print(e)
                with self.assertRaises(ValueError):
                    raise e


if __name__ == "__main__":
    unittest.main()