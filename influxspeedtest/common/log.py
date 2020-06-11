import logging
import sys


class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, above=True):
        self.passlevel = passlevel
        self.above = above

    def filter(self, record):
        if self.above:
            return record.levelno >= self.passlevel
        else:
            return record.levelno <= self.passlevel


def log_setup(logging_level="INFO"):
    log = logging.getLogger(__name__)
    log.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    general_handler = logging.StreamHandler(sys.stdout)
    general_filter = SingleLevelFilter(logging.INFO, False)
    general_handler.setFormatter(formatter)
    general_handler.addFilter(general_filter)
    log.addHandler(general_handler)

    error_handler = logging.StreamHandler(sys.stderr)
    error_filter = SingleLevelFilter(logging.WARNING)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(error_filter)
    log.addHandler(error_handler)

    log.propagate = False
    return log
