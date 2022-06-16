import os
import sys

NAME = 'CurseForgeModpackDownloader'
NAME_WITH_SPACE = 'CurseForge Modpack Downloader (CMPDL)'

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS')
else:
    BASE_DIR = os.getcwd()


class PATH:
    BASE_DIR = BASE_DIR
    ICON_PATH = os.path.join(BASE_DIR, 'icon.ico')
    TEMP_DIR_PATH = os.path.join(BASE_DIR, f'.{NAME}')
    LOG_FILE_NAME = f'{NAME}.log'


class WINDOW:
    WIDTH = 1200
    HEIGHT = 600
    SIZE = f'{WIDTH}x{HEIGHT}'


class SEARCH:
    VERSIONS = ['', '1.10.2', '1.12.2', '1.16.5', '1.18.2']
    SORT = {
        'Name': 3,
        'Popularity': 1,
        'Total Downloads': 5
    }
