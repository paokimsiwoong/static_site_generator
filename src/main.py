import os, shutil

from static_utils import copy_static_to_public, generate_page

def main():
    # print(os.getcwd())
    # /home/paokimsiwoong/workspace/github.com/paokimsiwoong/static_site_generator
    # @@@ 확인해보면 이 main.py이 있는 src 폴더가 아니라
    # @@@ 루트폴더의 경로를 보여준다

    # print(os.path.exists("public/"))

    path_to_static = "static/"
    path_to_public = "public/"


    if os.path.exists(path_to_public):
        shutil.rmtree(path_to_public)
    # 이전에 생성한 public 폴더가 남아 있으면 삭제 

    if not os.path.exists(path_to_public):
        os.mkdir(path_to_public)
    # 새로 public 폴더 생성

    copy_static_to_public(path_to_static, path_to_public)

    path_to_content = "content/index.md"
    path_to_template = "template.html"
    path_to_dest = "public/index.html"

    generate_page(path_to_content, path_to_template, path_to_dest)


if __name__ == "__main__":
    main()