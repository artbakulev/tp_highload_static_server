import asyncio
import logging

from app.config.Config import Config

config = Config('configs.yaml')

if __name__ == '__main__':
    from app.server.Server import Server
    from app.server.Worker import Worker

    loop = asyncio.get_event_loop()
    server = Server(config, loop)
    server.connect()

    workers = [Worker(loop, server.connection, config=config) for _ in range(config.get_int('workers_num', fallback=8))]
    asyncio.gather(*[loop.create_task(worker.run()) for worker in workers])
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('shutting down...')
        [worker.stop() for worker in workers]
        server.connection.shutdown()
