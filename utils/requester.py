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
    BASE_URL = 'https://api.curseforge.com'

    @staticmethod
    def get(url: str, params: Dict[str, Any] = None) -> Response:
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
        headers = {
            'Accept': 'application/json',
            'x-api-key': '*'
        }
        request = Request(url, headers=headers, method='GET')
        return Response(urlopen(request))

    def get_mod_file(self, project_id, file_id):
        return self.get(f'{self.BASE_URL}/v1/mods/{project_id}/files/{file_id}')

    def search_modpack(
            self,
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
        return self.get(f'{self.BASE_URL}/v1/mods/search', params=params)

    def files(self, _id: int):
        """
        Get modpack files.
        :param _id: Modpack ID.
        :return: Response.
        """
        return self.get(f'{self.BASE_URL}/v1/mods/{_id}/files')
