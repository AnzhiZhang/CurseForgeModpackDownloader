import os

from utils.constant import PATH
from utils.factory import Factory
from utils.window.main import Main


def main():
    if not os.path.isdir(PATH.TEMP_DIR_PATH):
        os.mkdir(PATH.TEMP_DIR_PATH)

    factory = Factory()
    Main(factory).main()


if __name__ == '__main__':
    main()
