import logging
import os


def get_filename(f):
    """
    Returns the current filename as a string

    Args:
        f: __file__ from the client cot
    Returns:
        str
    """
    name, _ = os.path.splitext(f)
    return name


def get_logger(module):
    """
    Returns a configured standard library `logger`

    Args:
        module (__name__) of the client code calling this function
    """
    logger = logging.getLogger(module)
    logger.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
