from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    my_node = TextNode("testing...", TextType.ITALIC, "https://www.test.ttt")
    print(my_node)

if __name__ == "__main__":
    main()