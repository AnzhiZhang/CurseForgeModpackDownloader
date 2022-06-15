NAME = 'CurseForgeModpackDownloader'
NAME_WITH_SPACE = 'CurseForge Modpack Downloader (CMPDL)'


class PATH:
    ICON_PATH = 'icon.ico'
    LOG_FILE_NAME = f'{NAME}.log'
    TEMP_DIR_PATH = f'.{NAME}'


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
