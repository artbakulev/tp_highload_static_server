import logging
import mimetypes
from collections import OrderedDict
import os
import socket
import asyncio

from app.decorators import with_connection

STATUS_MESSAGES = {
    200: 'OK',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
}


class Response:
    def __init__(self, config, protocol: str = 'HTTP/1.1', status: int = 200, headers: list = None,
                 path_to_file: [str, None] = None):
        self.config = config
        self.protocol = protocol
        self.status = status
        self.headers = headers if headers is not None else {}
        self.path_to_file = path_to_file
        self.raw = None
        self.max_socket_size = self.config.get_int('max_socket_size', fallback=1024)
        if self.path_to_file is not None:
            self.add_mime_headers()

    def add_mime_headers(self):
        file_size = os.path.getsize(self.path_to_file)
        mime_type, _ = mimetypes.guess_type(self.path_to_file)
        self.headers.update([{'Content-Type': mime_type},
                             {'Content-Length': file_size},
                             {'Connection': 'keep-alive'}])

    @with_connection
    async def send(self, loop: asyncio.AbstractEventLoop, conn: socket.socket):
        await loop.sock_sendall(conn, self.raw if self.raw is not None else self.format())
        if self.path_to_file is not None:
            with open(self.path_to_file, 'rb') as f:
                await loop.sock_sendall(conn, f.read(self.max_socket_size))
        conn.close()

    def format(self) -> bytes:
        self.raw = f'{self.protocol} {self.status} {STATUS_MESSAGES[self.status]}\r\n'
        self.raw += '\r\n'.join([f'{k}: {v}' for k, v in self.headers]) + '\r\n\r\n'
        self.raw = self.raw.encode('utf-8')
        return self.raw
