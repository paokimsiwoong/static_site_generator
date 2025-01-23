import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Both test functions and file names must start with test_ 
    # to be discoverable by unittest
    # ==> 파일이름 : test_****.py, 함수이름 : def test_****(self):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertTrue(node.__repr__() == 'LeafNode(a, Click me!, None,  href="https://www.google.com")')
        # f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

    def test_to_html(self):
        node = LeafNode(tag = "p", value="test")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode(tag=None, value="raw")

        self.assertTrue(
            node.to_html() == "<p>test</p>" and
            node2.to_html() == '<a href="https://www.google.com">Click me!</a>' and
            node3.to_html() == "raw"
            )
        
        node4 = LeafNode(tag = "p", value="")
        with self.assertRaises(ValueError):
            node4.to_html()
        # value 값이 비정상일 때 valueerror 잘 나오는지 확인


if __name__ == "__main__":
    unittest.main()