import os
import sys
import shutil

from utils.constant import PATH
from utils.factory import Factory
from utils.window.main import Main


def main():
    if not os.path.isdir(PATH.DATA_DIR):
        os.mkdir(PATH.DATA_DIR)

    # Init downloading temp path
    if os.path.isdir(PATH.DOWNLOADING_DIR_PATH):
        shutil.rmtree(PATH.DOWNLOADING_DIR_PATH)
    os.mkdir(PATH.DOWNLOADING_DIR_PATH)

    factory = Factory()

    # Set debug mode
    if '--debug' in sys.argv:
        factory.logger.set_debug(True)

    # Start main window
    Main(factory).main()

    # Clear downloading temp path
    shutil.rmtree(PATH.DOWNLOADING_DIR_PATH)


if __name__ == '__main__':
    main()
