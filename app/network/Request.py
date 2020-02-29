from app.network.Response import Response


class Request:
    DELIMITER = '\r\n'
    HEADERS_DELIMITER = ': '

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
            k, v = parts[i].split(self.HEADERS_DELIMITER)
            self.headers.update({k: v})

    def validate_request(self) -> [Response, bool]:
        if self.method not in self.config.get_list('allowed_methods'):
            return Response(method=self.method, status=405), False
