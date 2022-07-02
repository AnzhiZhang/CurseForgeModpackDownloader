import logging


class Logger:
    format = logging.Formatter(
        '[%(asctime)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def __init__(self, name: str, file_path: str):
        # Logger
        self.logger = logging.getLogger(name)
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
