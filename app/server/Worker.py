import logging
import socket as s
import asyncio

from app.network.Response import Response
from app.network.Request import Request


class Worker:
    def __init__(self, loop: asyncio.AbstractEventLoop, socket, config=None):
        self.config = config
        self.socket: s.socket = socket
        self.loop: asyncio.AbstractEventLoop = loop
        self.is_run = True

    async def start(self, executor):
        await self.loop.run_in_executor(
            executor, self.run()
        )

    async def run(self):
        while self.is_run:
            conn, _ = await self.loop.sock_accept(self.socket)
            await self.loop.create_task(self.handle(conn))

    async def handle(self, conn):
        request = await self.loop.sock_recv(conn, self.config.get_int('max_socket_size', fallback=1024))
        request = Request(request.decode('utf-8'), config=self.config)
        response = await request.validate_request()
        if response is None:
            response = Response(self.config, method=request.method, status=200, path_to_file=request.url)
        await response.send(self.loop, conn)
        conn.close()

    def stop(self):
        self.is_run = False
        self.socket.close()
