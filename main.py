#import imp
import os
from re import I
import shutil

from utils.constant import PATH
from utils.window.main import windows
from utils.window.main import linux
import platform

# It Seems Run It Via Code It Is A Lot Faster Than The Packed Version? Am I Wrong?


def main():
    # 清理临时文件夹
    # It Seems Temp Folder Works , But I Don't Where It is Probably /tmp?
    if os.path.isdir(PATH.TEMP_DIR_PATH):
        shutil.rmtree(PATH.TEMP_DIR_PATH)
    os.mkdir(PATH.TEMP_DIR_PATH)

    if(platform.system() == 'Windows'):
        windows()
    else:
        linux()

    shutil.rmtree(PATH.TEMP_DIR_PATH)


if __name__ == '__main__':
    main()
