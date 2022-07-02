import os

import yaml

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from utils.factory import Factory

from utils.constant import PATH


class Language:
    def __init__(self, factory: 'Factory'):
        self.__data: Dict[str, Dict[str, str]] = {}
        self.__lang = factory.config['language']
        self.__load()

    def __load(self):
        for i in os.listdir(PATH.LANG_DIR_PATH):
            path = os.path.join(PATH.LANG_DIR_PATH, i)
            with open(path, encoding='utf-8') as f:
                self.__data[os.path.splitext(i)[0]] = yaml.safe_load(f)

    def translate(self, key: str,  *args) -> str:
        """
        Translate words from key.
        :param key: Key of words.
        :param lang: Language name.
        :return: Words.
        """
        return self.__data.get(self.__lang).get(key).format(*args)

    def get_languages_list(self) -> List[str]:
        """
        Get languages list.
        :return: Language name list.
        """
        return list(self.__data.keys())