from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # tag
        # A string representing the HTML tag name 
        # (e.g. "p", "a", "h1", etc.)
        # children
        # A list of HTMLNode objects representing the children of this node
        # props
        # A dictionary of key-value pairs representing the attributes of the HTML tag. 
        # For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        # => html 파일에서는 <link rel="stylesheet" href="styles.css"> 처럼
        # <tagname k1=v1 k2=v2> 형태
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
