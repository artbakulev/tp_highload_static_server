import os

from app.network.Response import Response


class Request:
    DELIMITER = '\r\n'
    HEADERS_DELIMITER = ': '
    INDEX_FILE = 'index.html'

    def __init__(self, raw, config=None):
        self.method = None
        self.protocol = None
        self.url = None
        self.headers = {}
        self._parse_request(raw)
        self.config = config

    def _parse_request(self, raw: str):
        parts = raw.split(self.DELIMITER)
        self.method, self.url, self.protocol = parts[0].split(' ')
        for i in range(1, len(parts)):
            try:
                k, v = parts[i].split(self.HEADERS_DELIMITER)
                self.headers.update({k: v})
            except ValueError:
                pass

    def validate_request(self) -> Response:
        """:return: invalid response if does not validate"""
        if self.method not in self.config.get_list('allowed_methods'):
            return Response(self.config, status=405)

        if not self.url.endswith('/'):
            return Response(config=self.config, status=404)

        if self.url == '/':
            self.url = self.INDEX_FILE

        if self.url not in self.config.root:
            return Response(self.config, status=403)

        if os.path.isdir(self.url):
            self.url = os.path.join(self.url, self.INDEX_FILE)
            if not os.path.exists(self.url):
                return Response(self.config, status=403)

        if not os.path.exists(self.url):
            return Response(self.config, status=404)

        if not os.path.isfile(self.url):
            return Response(self.config, status=404)

        return None
