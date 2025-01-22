from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        # A string representing the HTML tag name 
        # (e.g. "p", "a", "h1", etc.)
        self.value = value
        # A string representing the value of the HTML tag 
        # (e.g. the text inside a paragraph)
        self.children = children
        # A list of HTMLNode objects representing the children of this node
        self.props = props
        # A dictionary of key-value pairs representing the attributes of the HTML tag. 
        # For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        # => html 파일에서는 <link rel="stylesheet" href="styles.css"> 처럼
        # <tagname k1=v1 k2=v2> 형태

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Every data member should be optional and default to None:
            # An HTMLNode without a tag will just render as raw text
            # An HTMLNode without a value will be assumed to have children
            # An HTMLNode without children will be assumed to have a value
            # An HTMLNode without props simply won't have any attributes
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    def to_html(self):
        raise NotImplementedError()
        # Child classes will override this method to render themselves as HTML.
    
    def props_to_html(self):
        # dict 상태의 props를 href="https://www.google.com" target="_blank"와 같이
        # html에 쓰이는 형태로 변환
        
        if self.props:
            # self.props 기본값인 None이 아닐때만 변환
            return reduce(lambda acc, x: f'{acc} {x[0]}="{x[1]}"', self.props.items(), "").lstrip()
            # @@@@ {acc} 바로 뒤에 빈칸 한칸 두는 방식으로 하면 맨 처음 key 앞에도 빈칸 생성됨
            # @@@@ ===> .lstrip() 필요  
        
        return None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"