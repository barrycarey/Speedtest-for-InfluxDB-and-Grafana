import time

from influxspeedtest.common import log
from influxspeedtest.common.exceptions import SpeedtestRunError
from influxspeedtest.common.utils import run_speed_test, convert_results
from influxspeedtest.config import config

from influxspeedtest.storage.influxv1_storage_handler import InfluxV1StorageHandler
from influxspeedtest.storage.influxv2_storage_handler import InfluxV2StorageHandler

storage_handlers = [InfluxV2StorageHandler()]

while True:

    for server in config.servers:
        try:
            results = run_speed_test(server)
        except SpeedtestRunError:
            time.sleep(config.delay)
            continue

        log.debug(results)
        for handler in storage_handlers:
            handler.save_results(results)

    log.debug('Waiting %s seconds until next test', config.delay)
    time.sleep(config.delay)
