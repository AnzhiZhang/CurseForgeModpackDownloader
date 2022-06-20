import os
import sys
import platform

NAME = 'CurseForgeModpackDownloader'
NAME_WITH_SPACE = 'CurseForge Modpack Downloader (CMPDL)'
LICENSE = (
    'Copyright © 2022 Andy Zhang and contributors\n'
    '本程序是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。\n'
    '发布该程序是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。\n'
    '你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 https://www.gnu.org/licenses/。'
)

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS')
else:
    BASE_DIR = os.getcwd()


class PATH:
    BASE_DIR = BASE_DIR
    WORKING_DIR = os.getcwd()

    if platform.system() == 'Windows':
        ICON_PATH = os.path.join(BASE_DIR, 'icon.ico')
    else:
        ICON_PATH = None

    TEMP_DIR_PATH = os.path.join(WORKING_DIR, f'.{NAME}')
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
