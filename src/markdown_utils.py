import re

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
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # 해답처럼 매번 각 타입을 "" str로 입력하지 말고 변수이름으로 지정가능하게 미리 만들어두기
    type_heading = "heading"
    type_code = "code"
    type_quote = "quote"
    type_unordered_list = "unordered_list"
    type_ordered_list = "ordered_list"
    type_paragraph = "paragraph"
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    type_checker = {
        r"^#+\s":type_heading,
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
