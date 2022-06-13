import os
import shutil

from utils.constant import PATH
from utils.window.main import Main


def main():
    # 清理临时文件夹
    if os.path.isdir(PATH.TEMP_DIR_PATH):
        shutil.rmtree(PATH.TEMP_DIR_PATH)
    os.mkdir(PATH.TEMP_DIR_PATH)

    Main()

    shutil.rmtree(PATH.TEMP_DIR_PATH)


if __name__ == '__main__':
    main()
