import os
import sys
import time
import platform

NAME = 'CurseForgeModpackDownloader'
NAME_WITH_SPACE = 'CurseForge Modpack Downloader (CMPDL)'

# Program and other files dir
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS')
else:
    BASE_DIR = os.getcwd()


class PATH:
    BASE_DIR = BASE_DIR
    WORKING_DIR = os.getcwd()
    DATA_DIR = os.path.join(WORKING_DIR, f'.{NAME}')

    LANG_DIR_PATH = os.path.join(BASE_DIR, 'lang')

    # Icon is not supported on linux
    if platform.system() == 'Windows':
        ICON_PATH = os.path.join(BASE_DIR, 'icon.ico')
    else:
        ICON_PATH = None

    DOWNLOADING_DIR_PATH = os.path.join(DATA_DIR, 'downloading')
    LOG_FILE_PATH = os.path.join(
        DATA_DIR,
        time.strftime('%Y-%m.log', time.localtime())
    )


class WINDOW:
    WIDTH = 1200
    HEIGHT = 600
    SIZE = f'{WIDTH}x{HEIGHT}'


class CONFIG:
    FILE_PATH = os.path.join(PATH.DATA_DIR, 'config.yml')
    DEFAULT = {
        'language': 'en-us',
        'curseForgeAPIKey': ''
    }


# Available search params
class SEARCH:
    VERSIONS = ['', '1.10.2', '1.12.2', '1.16.5', '1.18.2']
    SORTING = {
        'Name': [4, 'asc'],
        'Popularity': [2, 'desc'],
        'Total Downloads': [6, 'desc']
    }
