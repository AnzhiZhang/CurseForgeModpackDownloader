import logging


class Logger:
    format = logging.Formatter(
        '[%(asctime)s] [%(levelname)s]: [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def __init__(self, name: str, file_path: str):
        # Logger
        self.debug_mode = False
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

    def set_debug(self, debug: bool = False) -> None:
        """
        Set debug mode to on or off.
        :param debug: Turn on debug mode if it is True, off otherwise.
        """
        if debug:
            self.debug_mode = True
            self.logger.setLevel(logging.DEBUG)
            self.ch.setLevel(logging.DEBUG)
            self.fh.setLevel(logging.DEBUG)
        else:
            self.debug_mode = False
            self.logger.setLevel(logging.INFO)
            self.ch.setLevel(logging.INFO)
            self.fh.setLevel(logging.INFO)

    def close(self) -> None:
        """
        Close log file for clean logger.
        """
        self.fh.close()
        self.logger.removeHandler(self.fh)
