from enum import Enum

class TextType(Enum):
    RAW = "Raw"
    # int대신 str을 쓰면 TextType.RAW.value로 str값을 얻을 수 있다
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes 
    # split되기 전인 TextNode들의 리스트

    # delimiter
    # split할 기준

    # text_type
    # delimiter로 감싸인 노드의 새 text_type 

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.RAW:
            new_nodes.append(old_node)
            # 이미 완료된 부분은 그대로 리스트에 추가
            continue

        split_texts = old_node.text.split(delimiter)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@ 해답에서 발견한 부분 @@
        # delimiter 두개씩 제대로 짝지어져 있지 않는 에러가 있으면 raise 하기
        if len(split_texts) % 2 == 0:
        # 제대로 짝지어져 있으면 len은 반드시 홀수 값
            raise ValueError("Invalid markdown, formatted section not closed")
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        for i, text in enumerate(split_texts):
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # @@ 해답에서 발견한 부분 @@
            # 원래는 if i % 2 == 0: 안에 있었지만
            # ''나 **, **** 같은 경우도 있을 수 잇으므로 위치 변경
            if len(text) == 0:
            # "" 제거
                continue
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            if i % 2 == 0:
            # 지정한 delimiter에 감싸이지 않은 부분의 index는 항상 짝수
                    new_nodes.append(TextNode(text, TextType.RAW))
            else:
            # 지정한 delimiter에 감싸인 부분의 index는 항상 홀수
                new_nodes.append(TextNode(text, text_type))

    return new_nodes