import logging


def with_connection(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BrokenPipeError as e:
            logging.error(e)
            kwargs['conn'].close()

    return wrapper
