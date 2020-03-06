import asyncio
import logging
import multiprocessing
import concurrent.futures
from concurrent.futures.process import ProcessPoolExecutor

import uvloop

from app.config.Config import Config

config = Config('configs.yaml')

if __name__ == '__main__':
    from app.server.Server import Server
    from app.server.Worker import Worker

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    server = Server(config)
    server.connect()
    workers = [Worker(server.connection, config=config) for _ in range(config.get_int('cpu_num', fallback=2))]
    for worker in workers:
        worker.start()
    try:
        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        for worker in workers:
            worker.terminate()
        server.connection.close()
