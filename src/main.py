import os, shutil


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


if __name__ == "__main__":
    main()