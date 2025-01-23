import unittest

from parentnode import ParentNode
from leafnode import LeafNode

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