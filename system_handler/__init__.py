from .client import Client
from .error import Error
from .AESCipher import AESCiphers
from .file import File

import logging
def make_log(name=None):
    logger = logging.getLogger(name)
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
    if name == None: name = "root"
    handler = logging.FileHandler(filename=f'{name}.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('[%(levelname)s | %(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S'))
    logger.addHandler(handler)

    return logger

web_logging = make_log("ApiServer")
