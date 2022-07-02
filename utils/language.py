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

    def translate(self, key: str, *args, lang=None) -> str:
        """
        Translate words from key.
        :param key: Key of words.
        :param lang: Language name.
        :return: Words.
        """
        if lang is None:
            lang = self.__lang
        return self.__data.get(lang).get(key).format(*args)

    def get_languages(self) -> Dict[str, str]:
        """
        Get languages data.
        :return: A dict which key is language key and value is the name.
        """
        return {key: value['langName'] for key, value in self.__data.items()}
