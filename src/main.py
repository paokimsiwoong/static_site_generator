from textnode import TextType, TextNode

def main():
    my_node = TextNode("testing...", TextType.ITALIC, "https://www.test.ttt")
    print(my_node)

if __name__ == "__main__":
    main()