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
            return reduce(lambda acc, x: f'{acc} {x[0]}="{x[1]}"', self.props.items(), "")
            # @@@@ {acc} 바로 뒤에 빈칸 한칸 두는 방식으로 하면 맨 처음 key 앞에도 빈칸 생성됨
            # @@@@ ===> .lstrip() 필요??? => 없다. 합쳐질 때, tag str 뒤에 빈칸 한개 필요하므로 그대로 두기
        
        return ""

    def __repr__(self):
        if self.props:
            return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, None)"
        # @@@ {self.__class__.__name__}로 클래스 이름을 불러와서 표시하지 않으면
        # @@@ 상속받은 클래스마다 __repr__을 override해서 이름을 수정해야한다


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # leaf 노드나 다른 parent 노드들을 담을 노드가 되어야 하므로
        # tag와 children는 필수, value는 삭제
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A parent node must have a tag")
        
        if not self.children:
            raise ValueError("A parent node must have a children")
        
        def to_html_if_node(x):
            if not isinstance(x, HTMLNode):
                raise TypeError("A child must be an instance of HTMLNode")
            # self.children 안에는 HTMLNode를 상속한 노드들만 속해 있는지 확인하기
            
            return x.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{"".join(map(to_html_if_node, self.children))}</{self.tag}>"
        # children안의 모든 종속 노드들의 태그들을 합쳐서 이 ParentNode 태그 안에 넣기
