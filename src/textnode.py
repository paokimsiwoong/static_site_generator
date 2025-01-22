from enum import Enum

class TextType(Enum):
    NORMAL = "Normal"
    # int대신 str을 쓰면 TextType.NORMAL.value로 str값을 얻을 수 있다
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        # The text content of the node
        self.text_type = text_type
        # The type of text this node contains, 
        # which is a member of the TextType enum.
        self.url = url
        # The URL of the link or image, if the text is a link. 
        # Default to None if nothing is passed in.
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    # @@@ __str__ 이나 __repr__은 프린트될 내용들을 print가 아니라 return 해야 한다