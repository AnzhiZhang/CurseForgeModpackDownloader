import os
import yaml

from utils.constant import CONFIG


class Config(dict):
    def __init__(self):
        if os.path.isfile(CONFIG.FILE_PATH):
            with open(CONFIG.FILE_PATH, encoding='utf-8') as f:
                super().__init__(yaml.safe_load(f))
        else:
            super().__init__(CONFIG.DEFAULT)
            self.save()

    def save(self):
        """Save data"""
        with open(CONFIG.FILE_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(self.copy(), f)
