# 本文件是 CurseForgeModpackDownloader 的一部分。

# CurseForgeModpackDownloader 是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 通用公共许可证修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

# 发布 CurseForgeModpackDownloader 是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 通用公共许可证，了解详情。

# 你应该随程序获得一份 GNU 通用公共许可证的复本。如果没有，请看 <https://www.gnu.org/licenses/>。
import logging


class Logger:
    format = logging.Formatter(
        '[%(asctime)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def __init__(self, file_path: str):
        # Logger
        self.logger = logging.getLogger('CurseForgeModpackDownloader')
        self.logger.setLevel(logging.INFO)

        # Console Handler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)
        self.ch.setFormatter(self.format)
        self.logger.addHandler(self.ch)

        # File handler
        self.fh = logging.FileHandler(file_path, encoding='utf-8')
        self.fh.setLevel(logging.INFO)
        self.fh.setFormatter(self.format)
        self.logger.addHandler(self.fh)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.exception = self.logger.exception

    def close(self):
        self.fh.close()
        self.logger.removeHandler(self.fh)
