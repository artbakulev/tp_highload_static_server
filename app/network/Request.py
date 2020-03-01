import logging
import os
from urllib import parse

from app.network.Response import Response


class Request:
    DELIMITER = '\r\n'
    HEADERS_DELIMITER = ': '
    INDEX_FILE = 'index.html'
    ALLOWED_METHODS = ['GET', 'HEAD']

    def __init__(self, raw, config=None):
        self.method = None
        self.protocol = None
        self.url = None
        self._parse_request(raw)
        self.config = config

    def _parse_request(self, raw: str):
        parts = raw.split(self.DELIMITER)
        try:
            self.method, self.url, self.protocol = parts[0].split(' ')
            self.url = parse.unquote(self.url)
            if '?' in self.url:
                self.url = self.url[:self.url.index('?')]
        except ValueError:
            pass

    async def validate_request(self) -> Response:
        """:return: invalid response if does not validate"""
        if self.method not in self.ALLOWED_METHODS:
            return Response(self.config, status=405)

        if '/../' in self.url:
            return Response(self.config, status=403)

        if self.url == '/':
            self.url = os.path.join(self.config.root, self.INDEX_FILE)
        else:
            self.url = self.url.lstrip('/')
            self.url = os.path.join(self.config.root, self.url)

        if os.path.isdir(self.url):
            self.url = os.path.join(self.url, self.INDEX_FILE)
            if not os.path.exists(self.url):
                return Response(self.config, status=403)

        if not os.path.isfile(self.url):
            return Response(self.config, status=404)

        return None
