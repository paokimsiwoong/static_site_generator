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