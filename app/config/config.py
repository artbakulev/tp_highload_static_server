import logging


class Config:
    def __init__(self, path):
        self.path = path
        self.parse()
        self.init()

    def parse(self):
        pass

    def get_str(self, key, fallback=None) -> str:
        pass

    def get_int(self, key, fallback=None) -> int:
        pass

    def get_list(self, key, fallback=None) -> list:
        pass

    def init(self):
        pass
