import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Both test functions and file names must start with test_ 
    # to be discoverable by unittest
    # ==> 파일이름 : test_****.py, 함수이름 : def test_****(self):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertTrue(node.__repr__() == 'LeafNode(a, Click me!, None,  href="https://www.google.com")')
        # f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
    def test_props_to_html(self):
        # <a href="https://www.boot.dev">backend</a>
        node = LeafNode(tag="a", value="backend", props={"href":"https://www.boot.dev"})
        # print(node.props_to_html())
        self.assertTrue(node.props_to_html() == ' href="https://www.boot.dev"')

    def test_to_html(self):
        node = LeafNode(tag = "p", value="test")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode(tag=None, value="raw")

        self.assertTrue(
            node.to_html() == "<p>test</p>" and
            node2.to_html() == '<a href="https://www.google.com">Click me!</a>' and
            node3.to_html() == "raw"
            )


if __name__ == "__main__":
    unittest.main()