import socket as s
import asyncio

from app.network.Response import Response
from app.network.Request import Request


class Worker:
    def __init__(self, config, socket, loop):
        self.config = config
        self.socket: s.socket = socket
        self.loop: asyncio.AbstractEventLoop = loop
        self.is_run = True

    async def run(self):
        while self.is_run:
            conn, address = await self.loop.sock_accept(self.socket)
            await asyncio.create_task(self.handle(conn, address))

    async def handle(self, conn, address):
        request = await self.loop.sock_recv(conn, self.config.get_int('max_socket_size', fallback=1024))
        request = Request(request.decode('utf-8'))
        invalid_response = request.validate_request()
        if invalid_response is not None:
            await self.loop.sock_sendall(conn, str(invalid_response).encode('utf-8'))
            await self.loop.sock_sendall(conn, None)
            conn.close()
            return
        response = Response(method=request.method, )

    def stop(self):
        self.is_run = False
