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
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    pool = ProcessPoolExecutor(max_workers=config.get_int('cpu_num', fallback=2))
    workers = [Worker(loop, server.connection, config=config) for _ in range(config.get_int('cpu_num', fallback=2))]
    asyncio.gather(*[loop.create_task(worker.run()) for worker in workers])
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('shutting down...')
        [worker.stop() for worker in workers]
        server.connection.close()
