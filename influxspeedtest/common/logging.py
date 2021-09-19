import logging
import os
import sys

from influxspeedtest.common.logging.logfilters import SingleLevelFilter

default_format = '%(asctime)s - %(module)s:%(funcName)s:%(lineno)d - %(levelname)s: %(message)s'

def configure_logger(name: str = None, fmt: str = None, filters=None) -> logging.Logger:
    if filters is None:
        filters = []
    log = logging.getLogger(name or '')
    log.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))
    log.handlers = []
    formatter = logging.Formatter(fmt or default_format)
    general_handler = logging.StreamHandler(sys.stdout)
    general_handler.setFormatter(formatter)
    general_handler.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))
    error_handler = logging.StreamHandler(sys.stderr)
    error_filter = SingleLevelFilter(logging.WARNING)
    error_handler.setFormatter(formatter)
    for fltr in filters:
        general_handler.addFilter(fltr)
        error_handler.addFilter((fltr))
    general_handler.addFilter(SingleLevelFilter(logging.INFO, False))
    error_handler.addFilter(SingleLevelFilter(logging.WARNING))
    log.addHandler(general_handler)
    log.addHandler(error_handler)
    return log
