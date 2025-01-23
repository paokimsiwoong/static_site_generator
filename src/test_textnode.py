import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()