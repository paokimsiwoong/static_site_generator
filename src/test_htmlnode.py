import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Both test functions and file names must start with test_ 
    # to be discoverable by unittest
    # ==> 파일이름 : test_****.py, 함수이름 : def test_****(self):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def test_repr(self):
        node = HTMLNode(tag = "p", value="test")
        self.assertTrue(node.__repr__() == "HTMLNode(p, test, None, None)")
        # f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
    def test_props_to_html(self):
        # <a href="https://www.boot.dev">backend</a>
        node = HTMLNode(tag="a", value="backend", props={"href":"https://www.boot.dev"})
        # print(node.props_to_html())
        self.assertTrue(node.props_to_html() == 'href="https://www.boot.dev"')

    def test_to_html(self):
        node = HTMLNode(tag = "p", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()
        # self.assertRaises 함수를 with을 이용해 써서 
        # 지정한 exception이 잘 나오는지 확인 가능
        # ===>
        # with self.assertRaises(exception이름):
            # 지정한 exception이 나올지 확인할 코드


if __name__ == "__main__":
    unittest.main()