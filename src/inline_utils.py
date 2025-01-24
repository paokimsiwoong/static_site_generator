import re

from textnode import TextNode, TextType

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


def split_nodes_image(old_nodes):
    # @@@@ re.split을 활용해 extract_markdown_images 함수 미사용 @@@@
    # old_nodes 
    # split되기 전인 TextNode들의 리스트

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.RAW:
            new_nodes.append(old_node)
            # 이미 완료된 부분은 그대로 리스트에 추가
            continue
        
        cur = old_node.text
        while True:
            if len(cur) == 0:
                break

            split_texts = re.split(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", cur, 1)
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
            # re.split은 delimiter안의 () 그룹된 부분을 지우지 않고 추가한다
            # ===> maxsplit이 1인 경우 [앞부분, (g1), (g2), 뒷부분]
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
            # re.split(pattern, text, maxsplit, flag)

            if len(split_texts) == 1:
                cur = split_texts[0]
                break

            if len(split_texts[0]) > 0:
                new_nodes.append(TextNode(split_texts[0], TextType.RAW))
            new_nodes.append(TextNode(split_texts[1], TextType.IMAGE, split_texts[2]))

            cur = split_texts[-1]

        if len(cur) > 0:
            # 마지막 match 뒤부분이 공백이 아닌 경우
            new_nodes.append(TextNode(cur, TextType.RAW))

    return new_nodes


def split_nodes_link(old_nodes):
    # @@@@ re.split을 활용해 extract_markdown_links 함수 미사용 @@@@
    # old_nodes 
    # split되기 전인 TextNode들의 리스트

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.RAW:
            new_nodes.append(old_node)
            # 이미 완료된 부분은 그대로 리스트에 추가
            continue
        
        cur = old_node.text
        while True:
            if len(cur) == 0:
                break

            split_texts = re.split(r"(?<!!)\[([^\[\]]*?)\]\(([^\(\)]*?)\)", cur, 1)
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
            # re.split은 delimiter안의 () 그룹된 부분을 지우지 않고 추가한다
            # ===> maxsplit이 1인 경우 [앞부분, (g1), (g2), 뒷부분]
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
            # re.split(pattern, text, maxsplit, flag)

            if len(split_texts) == 1:
                cur = split_texts[0]
                break

            if len(split_texts[0]) > 0:
                new_nodes.append(TextNode(split_texts[0], TextType.RAW))
            new_nodes.append(TextNode(split_texts[1], TextType.LINK, split_texts[2]))

            cur = split_texts[-1]

        if len(cur) > 0:
            # 마지막 match 뒤부분이 공백이 아닌 경우
            new_nodes.append(TextNode(cur, TextType.RAW))

    return new_nodes


def text_to_textnodes(text):
    raw_node = TextNode(text, TextType.RAW)

    split_nodes = split_nodes_delimiter([raw_node], "`", TextType.CODE)
    split_nodes = split_nodes_delimiter(split_nodes, "**", TextType.BOLD)
    split_nodes = split_nodes_delimiter(split_nodes, "*", TextType.ITALIC)
    split_nodes = split_nodes_image(split_nodes)
    split_nodes = split_nodes_link(split_nodes)

    return split_nodes


# def extract_markdown_images(text):
#     # matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
#     matches = re.findall(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
#     # []와 ()은 정규식에서 예약어이므로 문자로 쓰이려면 \ 필요 

#     # .은 정규식에서 \n을 제외한 모든 문자를 뜻한
#     # *는 바로 앞의 글자가 0번 이상 반복되는 경우 일치
#     # ===> .* 임의 길이의 한줄(\n은 없으므로) 문자열(0이상)

#     # ?는 수량자(*, + 등) 뒤에 붙으면 게으른 수량자로 바꾼다
#     # 따라서, 만족하는 패턴이 발견되는 즉시 그 부분을 포함하면서 패턴을 만족하는 더 긴 문자열이 있어도
#     # 끝까지 확인하지 않고 이미 발견된 부분만 결과를 반환하고 다음으로 넘어가게 된다.
#     # ===> ?을 안붙이면 "test: [~](~~) and [*](**)" 에서
#     # ===> [~](~~) and [*](**) 전체가 하나로 찾아지지만 
#     # ===> ?을 붙이면 [~](~~), [*](**) 두개로 찾는다

#     # 예약어 ()는 ()안의 문자열을 그룹으로 묶어준다
#     # 이를 이용해 특정 그룹 부분만 추출하는 것도 가능하다
#     # findall을 사용하는 경우 검색 결과 : [(g1, g2, ...), (g1, g2, ...)] 
#     # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     # match, search, finditer 함수를 사용하면 match 객체를 반환하는데
#     # 이 때는 그 객체의 멤버 메소드 중 하나로 group을 사용해서 그룹별로 추출 가능하다
#     # .group(0)은 찾은 문자열 전체, 
#     # .group(1)은 첫번째 그룹에 해당되는 문자열
#     # .group(2)은 두번째 그룹에 해당되는 문자열
#     # .group(n)은 n번째 그룹에 해당되는 문자열
#     # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#     # ?는 단독으로 문자 뒤에 쓰이면 문자{0,1}과 동일 
#     # ({m,n}은 앞의 문자가 m번 이상 n번 이하면 일치)

#     return matches

# def extract_markdown_links(text):
#     # matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
#     matches = re.findall(r"(?<!!)\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
#     # extract_markdown_images와 거의 동일하지만
#     # 이번에는 []앞에 !이 있으면 제외해야한다
#     # ==> 부정형 전방 탐색 (?<!문자열) 사용

#     return matches

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 해답은 [^\[\]]와 [^\(\)]을
# 사용해서 *? 게으른 수량자 사용을 피함
# images
# r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
# regular links
# r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
# @@@@@@ [tbi wan]](https://i.imgur.com/fJRm4Vk.jpeg) 와 같이 []()가 여러번 쓰여서 오류난 경우를 .*?는 걸러주지 못한다
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# def split_nodes_image(old_nodes):
#     # old_nodes 
#     # split되기 전인 TextNode들의 리스트

#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.RAW:
#             new_nodes.append(old_node)
#             # 이미 완료된 부분은 그대로 리스트에 추가
#             continue

#         matches = extract_markdown_images(old_node.text)
#         if len(matches) == 0:
#             new_nodes.append(old_node)
#             # image가 없으면 그대로 추가하고 넘어가기
#             continue
        
#         cur = old_node.text
#         for i in range(len(matches)):
#             # 발견된 횟수만큼 split 진행하기

#             # split_texts = re.split(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", cur, 1)
#             # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
#             # re.split은 delimiter안의 () 그룹된 부분을 지우지 않고 추가한다
#             # ===> maxsplit이 1인 경우 [앞부분, (g1), (g2), 뒷부분]
#             # ==========> extract_markdown_images 함수 안쓰고 구현도 가능할 듯
#             # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
#             split_texts = re.split(r"!\[[^\[\]]*?\]\([^\(\)]*?\)", cur, 1)
#             # re.split(pattern, text, maxsplit, flag)

#             if len(split_texts[0]) > 0:
#                 new_nodes.append(TextNode(split_texts[0], TextType.RAW))
#             new_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))

#             cur = split_texts[1]

#         if len(cur) > 0:
#             # 마지막 match 뒤부분이 공백이 아닌 경우
#             new_nodes.append(TextNode(cur, TextType.RAW))

#     return new_nodes


# def split_nodes_link(old_nodes):
#     # old_nodes 
#     # split되기 전인 TextNode들의 리스트

#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.RAW:
#             new_nodes.append(old_node)
#             # 이미 완료된 부분은 그대로 리스트에 추가
#             continue

#         matches = extract_markdown_links(old_node.text)
#         if len(matches) == 0:
#             new_nodes.append(old_node)
#             # link가 없으면 그대로 추가하고 넘어가기
#             continue
        
#         cur = old_node.text
#         for i in range(len(matches)):
#             # 발견된 횟수만큼 split 진행하기

#             # split_texts = re.split(r"(?<!!)\[([^\[\]]*?)\]\(([^\(\)]*?)\)", cur, 1)
#             # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
#             # re.split은 delimiter안의 () 그룹된 부분을 지우지 않고 추가한다
#             # ===> maxsplit이 1인 경우 [앞부분, (g1), (g2), 뒷부분]
#             # ==========> extract_markdown_images 함수 안쓰고 구현도 가능할 듯
#             # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
#             split_texts = re.split(r"(?<!!)\[[^\[\]]*?\]\([^\(\)]*?\)", cur, 1)
#             # re.split(pattern, text, maxsplit, flag)

#             if len(split_texts[0]) > 0:
#                 new_nodes.append(TextNode(split_texts[0], TextType.RAW))
#             new_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))

#             cur = split_texts[1]

#         if len(cur) > 0:
#             # 마지막 match 뒤부분이 공백이 아닌 경우
#             new_nodes.append(TextNode(cur, TextType.RAW))

#     return new_nodes


