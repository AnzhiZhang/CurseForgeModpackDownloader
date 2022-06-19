import json
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from typing import Any, Dict
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


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
        'user-agent': ''
    }

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
    def download_url(cls, project_id, file_id):
        return cls.get(
            f'https://addons-ecs.forgesvc.net/api/v2/addon/'
            f'{project_id}/file/{file_id}/download-url'
        )

    @classmethod
    def search_modpack(
            cls,
            game_version: str = None,
            search_filter: str = None,
            sort: int = None,
            index: int = 0
    ):
        """
        Search modpacks.
        :param game_version: Game version string.
        :param sort: Sorting rule.
        :param search_filter: Filter to search, a string.
        :param index: Page index.
        :return: Response.
        """
        params = {
            'gameId': 432,
            'sectionId': 4471,
            'index': index
        }
        if game_version:
            params['gameVersion'] = game_version
        if search_filter:
            params['searchFilter'] = search_filter
        if sort:
            params['sort'] = sort
        return cls.get(
            'https://addons-ecs.forgesvc.net/api/v2/addon/search',
            params=params
        )

    @classmethod
    def files(cls, _id: int):
        """
        Get modpack files.
        :param _id: Modpack ID.
        :return: Response.
        """
        return cls.get(
            f'https://addons-ecs.forgesvc.net/api/v2/addon/{_id}/files'
        )
