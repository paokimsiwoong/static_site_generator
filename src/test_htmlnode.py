import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertTrue(node.props_to_html() == ' href="https://www.boot.dev"')

    def test_to_html(self):
        node = HTMLNode(tag = "p", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()
        # self.assertRaises 함수를 with을 이용해 써서 
        # 지정한 exception이 잘 나오는지 확인 가능
        # ===>
        # with self.assertRaises(exception이름):
            # 지정한 exception이 나올지 확인할 코드


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


class TestParentNode(unittest.TestCase):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Both test functions and file names must start with test_ 
    # to be discoverable by unittest
    # ==> 파일이름 : test_****.py, 함수이름 : def test_****(self):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def test_repr(self):
        # 복잡하게 nested 되도 __repr__ 잘 작동하는지 확인
        node = ParentNode("a", [LeafNode("p", "test"), ParentNode("b", [LeafNode("p", "test"), LeafNode("p", "test")])], {"href": "https://www.google.com"})
        # print(node)
        self.assertTrue(node.__repr__() == 'ParentNode(a, None, [LeafNode(p, test, None, None), ParentNode(b, None, [LeafNode(p, test, None, None), LeafNode(p, test, None, None)], None)],  href="https://www.google.com")')
        # f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

    def test_to_html(self):
        node = ParentNode("a", [LeafNode("p", "test"), ParentNode("b", [LeafNode("p", "test"), LeafNode("p", "test")])], {"href": "https://www.google.com"})

        # print(node.to_html())

        self.assertTrue(
            node.to_html() == '<a href="https://www.google.com"><p>test</p><b><p>test</p><p>test</p></b></a>'
            )
        
        node2 = ParentNode("a", [], {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            try:
                node2.to_html()
            except Exception as e:
                print(e)
                raise e

            # node2.to_html()
        # children 값이 비정상일 때 valueerror 잘 나오는지 확인

        node3 = ParentNode("a", [LeafNode("p", "test"), 3], {"href": "https://www.google.com"})
        with self.assertRaises(TypeError):
            # children안에 HTMLNode 계열이 아닌 것이 들어 있으면 TypeError가 나야한다
            node3.to_html()
        # children 값이 비정상일 때 valueerror 잘 나오는지 확인


if __name__ == "__main__":
    unittest.main()