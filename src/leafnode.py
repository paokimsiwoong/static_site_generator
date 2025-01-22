from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # tag
            # A string representing the HTML tag name 
            # (e.g. "p", "a", "h1", etc.)
        # value
            # A string representing the value of the HTML tag 
            # (e.g. the text inside a paragraph)
        # props
            # A dictionary of key-value pairs representing the attributes of the HTML tag. 
            # For example, a link (<a> tag) might have {"href": "https://www.google.com"}
            # => html 파일에서는 <link rel="stylesheet" href="styles.css"> 처럼
            # <tagname k1=v1 k2=v2> 형태
        # @@@@@@@@@ LeafNode는 Leaf이므로 children이 반드시 없고 value 값이 있어야 한다
        # @@@@@@@@@ (tag는 None이어도 raw text로 표현 가능하므로 None 입력이 가능하지만 기본값 설정을 지워서 반드시 tag 지정하도록 한다)
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        # leafnode의 데이터를 실제 html 코드로 반환하는 함수
        if not self.value:
            raise ValueError("A leaf node must have a value")

        if not self.tag:
            # tag가 없으면 raw text로 반환
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        # self.props_to_html()은 self.props가 None이면 ""반환
        # None이 아니면 " ~~~"로 맨 앞에 빈칸 한개가 있는 상태를 반환하므로 {self.tag}뒤에 빈칸 필요 없음 