import asyncio
import multiprocessing
import socket as s

from app.network.Request import Request
from app.network.Response import Response


class Worker(multiprocessing.Process):
    def __init__(self, socket, config=None):
        super().__init__()
        self.config = config
        self.socket: s.socket = socket
        self.loop: asyncio.AbstractEventLoop = None
        self.is_run = True
        self.is_stopped = False

    def run(self):
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.__run())
        except KeyboardInterrupt:
            self.loop.close()

    async def __run(self):
        while self.is_run:
            conn, _ = await self.loop.sock_accept(self.socket)
            conn.settimeout(self.config.get_int('timeout'))
            self.loop.create_task(self.handle(conn))

    async def handle(self, conn):
        request = await self.loop.sock_recv(conn, self.config.get_int('max_socket_size', fallback=1024))
        request = Request(request.decode('utf-8'), config=self.config)
        response = await request.validate_request()
        if response is None:
            response = Response(self.config, method=request.method, status=200, path_to_file=request.url)
        await response.send(self.loop, conn)
        conn.close()

    async def stop(self):
        self.is_run = False
