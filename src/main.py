import os, shutil

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def copy_static_to_public():
    # 루트 경로의 public 폴더를 초기화하고 static 폴더의 내용을 복사하는 함수 

    print(os.getcwd())
    # /home/paokimsiwoong/workspace/github.com/paokimsiwoong/static_site_generator
    # @@@ 확인해보면 이 main.py이 있는 src 폴더가 아니라
    # @@@ 루트폴더의 경로를 보여준다

    print(os.path.exists("public/"))

    path_to_public = "public/"
    path_to_static = "static/"


    if os.path.exists(path_to_public):
        shutil.rmtree(path_to_public)

    if not os.path.exists(path_to_public):
        os.mkdir(path_to_public)


def main():
    my_node = TextNode("testing...", TextType.ITALIC, "https://www.test.ttt")
    print(my_node)

    copy_static_to_public()


if __name__ == "__main__":
    main()