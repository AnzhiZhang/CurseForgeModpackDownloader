from utils.logger import Logger
from utils.config import Config
from utils.requester import Requester
from utils.constant import NAME, PATH


class Factory:
    def __init__(self):
        self.__logger = Logger(NAME, PATH.LOG_FILE_PATH)
        self.__config = Config()
        self.__requester = Requester(self)

    @property
    def logger(self):
        return self.__logger

    @property
    def config(self):
        return self.__config

    @property
    def requester(self):
        return self.__requester
