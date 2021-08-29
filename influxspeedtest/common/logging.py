import logging
import os
import sys

from influxspeedtest.common.logfilters import SingleLevelFilter
from influxspeedtest.config import config

log = logging.getLogger(__name__)
log.setLevel(os.getenv('LOG_LEVEL', config.log_level))
formatter = logging.Formatter('%(asctime)s - %(module)s:%(funcName)s:%(lineno)d - [%(process)d][%(threadName)s] - %(levelname)s: %(message)s')

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