from utils.config import Config
from utils.requester import Requester


class Factory:
    def __init__(self):
        self.__config = Config()
        self.__requester = Requester(self)

    @property
    def config(self):
        return self.__config

    @property
    def requester(self):
        return self.__requester
