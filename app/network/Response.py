import asyncio
import datetime
import logging
import mimetypes
import os
import socket

STATUS_MESSAGES = {
    200: 'OK',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
}


class Response:

    def __init__(self, config, method: str = 'GET', protocol: str = 'HTTP/1.1', status: int = 200,
                 path_to_file: [str, None] = None):
        self.config = config
        self.method = method
        self.protocol = protocol
        self.status = status
        self.headers = {'Connection': 'close', 'Server': 'artbakulev',
                        'Date': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
        self.path_to_file = path_to_file
        self.raw = None
        self.max_socket_size = self.config.get_int('max_socket_size')
        if self.path_to_file is not None:
            self.add_mime_headers()

    def add_mime_headers(self):
        file_size = os.path.getsize(self.path_to_file)
        mime_type, _ = mimetypes.guess_type(self.path_to_file)
        self.headers.update({'Content-Type': mime_type})
        self.headers.update({'Content-Length': file_size})

    async def send(self, loop: asyncio.AbstractEventLoop, conn: socket.socket = None):
        await loop.sock_sendall(conn, self.raw if self.raw is not None else self.format())
        if self.path_to_file is not None and self.method != 'HEAD':
            with open(self.path_to_file, 'rb') as f:
                batch = f.read(self.max_socket_size)
                try:
                    while len(batch) > 0:
                        await loop.sock_sendall(conn, batch)
                        batch = f.read(self.max_socket_size)
                except BrokenPipeError:
                    pass

    def format(self) -> bytes:
        self.raw = f'{self.protocol} {self.status} {STATUS_MESSAGES[self.status]}\r\n'
        self.raw += '\r\n'.join([f'{k}: {v}' for k, v in self.headers.items()]) + '\r\n\r\n'
        self.raw = self.raw.encode('utf-8')
        return self.raw
