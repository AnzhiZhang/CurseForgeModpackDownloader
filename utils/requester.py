# 本文件是 MinecraftModpackDownloader 的一部分。

# MinecraftModpackDownloader 是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

# 发布 MinecraftModpackDownloader 是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。

# 你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 <https://www.gnu.org/licenses/>。
from urllib.parse import quote
from urllib.request import Request, urlopen


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


class Requester:
    HEADERS = {
        'user-agent': ''
    }

    @classmethod
    def get(cls, url: str) -> Response:
        url = quote(url, safe=':/')
        request = Request(url, headers=cls.HEADERS)
        return Response(urlopen(request))

    @classmethod
    def download_url(cls, project_id, file_id):
        return cls.get(
            f'https://addons-ecs.forgesvc.net/api/v2/addon/'
            f'{project_id}/file/{file_id}/download-url'
        )
