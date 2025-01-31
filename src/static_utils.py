import os, shutil

from markdown_utils import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
        # .read()는 파일 내용 전체를 문자열로 반환
    with open(template_path, "r") as template_file:
        template = template_file.read()
        # .read()는 파일 내용 전체를 문자열로 반환
    
    html_str = markdown_to_html_node(markdown).to_html()
    # 마크다운을 html로 변환

    title = extract_title(markdown)
    # title만 추출

    content = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html_str)
    # place holder들을 알맞은 내용으로 치환하기

    os.makedirs("/".join(dest_path.split("/")[:-1]), exist_ok=True)
    # makedirs는 makedir과 다르게 지정한 경로를 만들기 위해 필요한 중간 경로들도 다 같이 생성해준다
    # ===> "./a/b/c" 에서 a와 b 경로가 없는 경우 makedir은 c경로 생성이 불가능하지만 makedirs는 a와 b를 생성하고 그 안에 문제 없이 c를 생성한다
    # exist_ok=False(기본값)일 경우 지정한 경로가 이미 있을 때 raise Exception
    # ==> True로 두면 raise 없이 넘어간다 
    # ===> 지정한 경로가 없을 때만 경로 생성
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # 해답에서는 os.path.dirname(dest_path)를 활용해 매우 간단하게 경로 str을 얻어낸다
    # dest_dir_path = os.path.dirname(dest_path)
    # if dest_dir_path != "":
    #     os.makedirs(dest_dir_path, exist_ok=True)
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # os.path.dirname()은 파일이 있는 경로를 반환하고
    # os.path.basename()은 파일이름을 반환한다
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # os.path.split()을 쓰면 
    # "경로", "파일이름.파일확장자"로 분리해 반환해주고
    # os.path.splitext()는
    # "경로/파일이름", "파일확장자"로 분리해 반환해준다
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    with open(dest_path, "w") as html_file:
        html_file.write(content)
        # html로 작성되어있는 content를 지정 경로에 생성한 html파일에 저장



def copy_static_to_public(cur_path_to_static, cur_path_to_public):
    # 루트 경로의 public 폴더를 초기화하고 static 폴더의 내용을 복사하는 함수 
    paths = os.listdir(cur_path_to_static)
    print(paths)

    for path in paths:
        new_path_to_static = os.path.join(cur_path_to_static, path)
        new_path_to_public = os.path.join(cur_path_to_public, path)
        # path는 파일또는 경로의 이름 => os.path.join으로 기존 경로와 합쳐주기

        if os.path.isfile(new_path_to_static):
            # 파일인 경우에는 바로 복사
            shutil.copy(new_path_to_static, new_path_to_public)
        else:
            # 파일이 아니라 경로인 경우 재귀를 이용해 내부로 들어가 복사 재개
            os.mkdir(new_path_to_public)
            # 디렉토리 생성
            copy_static_to_public(new_path_to_static, new_path_to_public)
            # 재귀 실행