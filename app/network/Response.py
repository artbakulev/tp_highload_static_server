import socket
import asyncio

from app.main import config


class Response:
    def __init__(self, method: str, status: int = 200, headers: [dict, None] = None, path_to_file: [str, None] = None):
        self.method = method
        self.status = status
        self.header = headers
        self.path_to_file = path_to_file

    async def send(self, loop: asyncio.AbstractEventLoop, conn: socket.socket):
        await loop.sock_sendall(conn, str(self))
        if self.path_to_file is not None:
            with open(self.path_to_file, 'r') as f:
                # TODO: наверняка есть async чтение из файла
                await loop.sock_sendall(conn, f.read(config.get_int('max_socket_size', fallback=1024)))

    def __str__(self):
        return ''.encode('utf-8')
