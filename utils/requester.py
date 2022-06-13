# 本文件是 CurseForgeModpackDownloader 的一部分。

# CurseForgeModpackDownloader 是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

# 发布 CurseForgeModpackDownloader 是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。

# 你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 <https://www.gnu.org/licenses/>。
import json
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from typing import Any, Dict


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
        :return: A Response object.
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
