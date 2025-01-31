import re

from htmlnode import LeafNode, ParentNode, text_node_to_html_node

from inline_utils import text_to_textnodes


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 해답처럼 매번 각 타입을 "" str로 입력하지 말고 변수이름으로 지정가능하게 미리 만들어두기
type_heading = "heading" # <h1~6> </h1~6>
type_code = "code" # <code> </code>
type_quote = "quote" # <blockquote> </blockquote>
type_unordered_list = "unordered_list" # <ul><li>첫라인</li><li>두번째라인</li></ul>
type_ordered_list = "ordered_list" # <ol><li>첫라인</li><li>두번째라인</li></ol>
type_paragraph = "paragraph" # <p> </p>
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def extract_title(markdown):
    # h1 header를 찾아 그 내용을 반환하는 함수

    blocks = markdown_to_blocks(markdown)
    # 마크다운 원문을 block들로 분리
    
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type != type_heading:
            continue

        lines = block.split("\n")
        # block의 여러 줄들을 분리해서 lines에 저장

        match = re.match(r"^(#{1,6})\s(.*)", lines[0])
        num_shop = len(match.group(1))
        # # 개수 확인

        if num_shop != 1:
            continue

        raw_lines = []

        raw_lines.append(match.group(2))
        # 첫번째 줄은 # 제거한 것을 입력
        raw_lines.extend(lines[1:])
        # 나머지는 그대로

        return "\n".join(raw_lines).strip()

        

    raise Exception("Invalid markdown, no title found")
    # h1 header 즉 "# ~~~" 꼴이 마크다운에 없으면 raise

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 해답은 엄청 단순하게 "\n"으로 나눈 후 line.startswith("# ") 사용
# def extract_title(md):
#     lines = md.split("\n")
#     for line in lines:
#         if line.startswith("# "):
#             return line[2:]
#     raise ValueError("No title found")
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def markdown_to_html_node(markdown):
    # 마크다운 원문을 모든 정보를 담은 HTMLNode로 변환해 반환하는 함수

    blocks = markdown_to_blocks(markdown)
    # 마크다운 원문을 block들로 분리

    block_nodes = []
    # 각 block들을 HTMLNode로 변환한 뒤 여기에 보관

    for block in blocks:
        block_type = block_to_block_type(block)
        # block의 타입 확인

        lines = block.split("\n")
        # block의 여러 줄들을 분리해서 lines에 저장

        block_node, raw_lines = block_type_to_htmlnode(block_type, lines)
        # block 타입에 맞는 HTML 노드 생성 및 타입을 알리는 마크다운 예약어를 제거한 raw_lines 반환

        children = raw_lines_to_childnodes(block_type, raw_lines)
        # block 안의 raw_line들을 HTMLNode로 변환 후 children에 저장

        block_node.children.extend(children)
        # block에 children 붙이기

        block_nodes.append(block_node)



    div_node = ParentNode("div", block_nodes)
    return div_node


def markdown_to_blocks(markdown):
    blocks = []
    # 함수 반환값(block str들을 담은 list)을 담을 리스트

    lines = markdown.strip().split("\n")
    # 줄나눔 기호 기준으로 split
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # 해답은 깔끔한 마크다운만 들어올걸 가정하고 있으므로 \n\n으로 split
    # ===> 나뉘어진 부분들이 바로 block이 됨 => .strip()만 하고 바로 blocks에 입력
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    block = []

    for line in lines:
        line = line.strip()
        # 각 라인 앞 뒤 공백 제거후 block에 입력
        if len(line) == 0:
            # block 사이의 공백 줄이 나올때마다
            if len(block) != 0:
                blocks.append("\n".join(block).strip())
                # block에 저장된 여러줄을 하나의 str으로 만들고 blocks에 입력
                block = []
            continue

        block.append(line)
        # 각 라인 앞 뒤 공백 제거후 block에 입력

    if len(block) != 0:
        blocks.append("\n".join(block).strip())

    return blocks


def block_to_block_type(block):
    # block을 입력받으면 해당 block의 타입을 알려주는 함수

    type_checker = {
        r"^#{1,6}\s":type_heading,
        r"^```(.|\n)+?```":type_code,
        r"^>\s":type_quote,
        r"^\*\s":type_unordered_list,
        r"^-\s":type_unordered_list,
        r"^[0-9]+\.\s":type_ordered_list,
        }
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # block이 여러줄인 경우 그 모든 줄들이 동일한 type인 것을 확인해야한다
    # ==> 아니면 그 block의 type은 paragraph
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    lines = block.split("\n")
    
    for k, v in type_checker.items():
        if isinstance(re.match(k, block),re.Match):
            if v == "heading" or v == "code":
                # heading이나 code는 모든 줄 앞에 기호가 붙지 않는다
                return v
            
            for line in lines:
                if not isinstance(re.match(k, line),re.Match):
                    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    # block이 여러줄인 경우 그 모든 줄들이 동일한 type인 것을 확인해야한다
                    # ==> 아니면 그 block의 type은 paragraph
                    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    return type_paragraph
            return v
        
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # 해답은
    # if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        # return block_type_heading
    # 과 같이 .startswith 함수사용
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        
    return type_paragraph


def block_type_to_htmlnode(block_type, lines):
    raw_lines = []
    if block_type == type_heading:
        match = re.match(r"^(#{1,6})\s(.*)", lines[0])
        num_shop = len(match.group(1))
        # # 개수 확인

        tag = f"h{num_shop}"
        # # 개수에 맞는 tag 작성

        raw_lines.append(match.group(2))
        # 첫번째 줄은 # 제거한 것을 입력
        raw_lines.extend(lines[1:])
        # 나머지는 그대로
    elif block_type == type_code:
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        tag = "pre"
        # code 블록은 <pre><code>~~~<br>~~<br>~~~~</code></pre> 구조
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        raw_lines = lines[1:-1]
        # 첫줄 ```과 마지막줄 ``` 제외
    elif block_type == type_quote:
        tag = "blockquote"

        for line in lines:
            raw_lines.append(line[2:])
            # >\s 제거
    elif block_type == type_unordered_list:
        tag = "ul"

        for line in lines:
            raw_lines.append(line[2:])
            # \*\s 또는 -\s 제거
    elif block_type == type_ordered_list:
        tag = "ol"

        for line in lines:
            match = re.match(r"^([0-9]+\.)\s(.*)", line)
            raw_lines.append(match.group(2))
            # [0-9]\.\s 제거
    else:
        tag = "p"
        raw_lines = lines[:]

    return ParentNode(tag, []), raw_lines


def raw_lines_to_childnodes(block_type, raw_lines):
    children = []

    if block_type in (type_unordered_list, type_ordered_list):
        # ul과 ol은 각 줄마다 li로 또 감싸줘야 한다
        for line in raw_lines:
            children.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(line)))))
            # text_to_textnodes 함수로 line을 TextNode들의 리스트로 만든 뒤, 
            # 각 TextNode들에 text_node_to_html_node 함수를 적용해 LeafNode로 변환
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # 해답과 같이 코드 블록은 inline 코드 블록과 구분되게
    # pre 태그로 한번 더 감싸주기
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    elif block_type == type_code:
        grand_children = []
        # <pre><code>~~~<br>~~<br>~~~~</code></pre> 과 같은 구조가 되어야 한다

        for i, line in enumerate(raw_lines):
            grand_children.extend(list(map(text_node_to_html_node, text_to_textnodes(line))))
            # 위와 동일하게 LeafNode 변환 후 리스트에 추가 (단 li 노드 없음)

            if i < (len(raw_lines) - 1):
                grand_children.append(LeafNode("br", ""))
                # 줄바꿈 <br> 노드도 각줄마다 마지막에 추가
                # 단 마지막 줄은 제외
        
        children.append(ParentNode("code", grand_children))
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    else:
        # 줄바꿈은 <br>
        for i, line in enumerate(raw_lines):
            children.extend(list(map(text_node_to_html_node, text_to_textnodes(line))))
            # 위와 동일하게 LeafNode 변환 후 리스트에 추가 (단 li 노드 없음)

            if i < (len(raw_lines) - 1):
                children.append(LeafNode("br", ""))
                # 줄바꿈 <br> 노드도 각줄마다 마지막에 추가
                # 단 마지막 줄은 제외


    return children