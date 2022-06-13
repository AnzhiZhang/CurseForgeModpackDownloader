NAME = 'CurseForgeModpackDownloader'


class PATH:
    LOG_FILE_NAME = f'{NAME}.log'
    TEMP_DIR_PATH = f'.{NAME}'


class SEARCH:
    VERSIONS = ['', '1.10.2', '1.12.2', '1.16.5', '1.18.2']
    SORT = {
        'Name': 3,
        'Popularity': 1,
        'Total Downloads': 5
    }
