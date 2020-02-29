import asyncio
import socket

from app.config.config import Config


class Server:
    def __init__(self, config: Config, loop: asyncio.AbstractEventLoop):
        self.host = config.get_str('host', fallback='127.0.0.1')
        self.port = config.get_int('port', fallback=8001)
        self.backlog = config.get_int('backlog', fallback=8)
        self.address = f'{self.host}:{self.port}'
        self.loop = loop
        self.connection = None

    def connect(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.bind((self.host, self.port))
        conn.listen(self.backlog)
        conn.setblocking(False)
        self.connection = conn

    @property
    def socket(self):
        return self.socket
