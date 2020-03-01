import logging
import os


class Config:
    DELIMITER = ': '

    def __init__(self, path):
        self.path = path
        self.raw = {}
        self.root = None
        self.parse()
        self.init()

    def parse(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            delimiter_index = line.index(self.DELIMITER)
            self.raw[line[:delimiter_index]] = line[delimiter_index + len(self.DELIMITER):].strip()

    def get(self, key):
        return self.raw.get(key, None)

    def get_str(self, key, fallback=None) -> str:
        raw = self.get(key)
        if raw is None and fallback is None:
            raise Exception(f'Invalid configs, key: {key}')
        return raw or fallback

    def get_int(self, key, fallback: int = None) -> int:
        raw = self.get(key)
        if raw is None and fallback is None:
            raise Exception(f'Invalid configs, key: {key}')
        return int(raw) or fallback

    def get_list(self, key, fallback: list = None) -> list:
        raw = self.get(key)
        if raw is None and fallback is None:
            raise Exception(f'Invalid configs, key: {key}')
        return raw.split(', ') or fallback

    def init(self):
        self.root = os.path.abspath(os.path.join(os.getcwd(), self.get_str('root_path', fallback='.')))
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            level=self.get_str('log_level', fallback='DEBUG'))
