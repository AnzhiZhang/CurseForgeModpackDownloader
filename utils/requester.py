import json
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from typing import Any, Dict, List


class Response:
    def __init__(self, response):
        self.__response = response
        self.__content = self.__response.read()
        self.__charset = self.headers.get_content_charset()

    @property
    def headers(self):
        return self.__response.headers

    @property
    def content(self):
        return self.__content

    @property
    def text(self):
        return self.content.decode(self.__charset)

    def json(self):
        return json.loads(self.content)


class Requester:
    HEADERS = {
        'Accept': 'application/json',
        'x-api-key': '*'
    }
    BASE_URL = 'https://api.curseforge.com'

    @classmethod
    def get(cls, url: str, params: Dict[str, Any] = None) -> Response:
        """
        Request using get method.
        :param url: URL.
        :param params: Parametric.
        :return: Response.
        """
        url = quote(url, safe=':/')

        # add params
        if params:
            url = url + '?' + urlencode(params)

        # send request
        request = Request(url, headers=cls.HEADERS, method='GET')
        return Response(urlopen(request))

    @classmethod
    def get_mod_file(cls, project_id, file_id):
        return cls.get(f'{cls.BASE_URL}/v1/mods/{project_id}/files/{file_id}')

    @classmethod
    def search_modpack(
            cls,
            game_version: str = None,
            search_filter: str = None,
            sorting: List = None,
            index: int = 0
    ):
        """
        Search modpacks.
        :param game_version: Game version string.
        :param search_filter: Filter to search, a string.
        :param sorting: Sorting rule, a list. First number is sort field and
            second string is order.
        :param index: Page index.
        :return: Response.
        """
        params = {
            'gameId': 432,
            'classId': 4471,
            'index': index
        }
        if game_version:
            params['gameVersion'] = game_version
        if search_filter:
            params['searchFilter'] = search_filter
        if sorting:
            params['sortField'] = sorting[0]
            params['sortOrder'] = sorting[1]
        return cls.get(f'{cls.BASE_URL}/v1/mods/search', params=params)

    @classmethod
    def files(cls, _id: int):
        """
        Get modpack files.
        :param _id: Modpack ID.
        :return: Response.
        """
        return cls.get(f'{cls.BASE_URL}/v1/mods/{_id}/files')
