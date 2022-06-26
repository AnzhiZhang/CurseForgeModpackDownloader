from utils.requester import Requester


class Factory:
    def __init__(self):
        self.__requester = Requester()

    @property
    def requester(self):
        return self.__requester
