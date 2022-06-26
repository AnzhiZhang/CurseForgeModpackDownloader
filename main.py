import os
import shutil

from utils.constant import PATH
from utils.factory import Factory
from utils.window.main import Main


def main():
    if not os.path.isdir(PATH.DATA_DIR):
        os.mkdir(PATH.DATA_DIR)
    if os.path.isdir(PATH.DOWNLOADING_DIR_PATH):
        shutil.rmtree(PATH.DOWNLOADING_DIR_PATH)
    os.mkdir(PATH.DOWNLOADING_DIR_PATH)

    factory = Factory()
    Main(factory).main()

    shutil.rmtree(PATH.DOWNLOADING_DIR_PATH)


if __name__ == '__main__':
    main()
