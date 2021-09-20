import os
import sys
import time

from influxspeedtest.common.exceptions import SpeedtestRunError, SpeedtestInstallFailure
from influxspeedtest.common.logging.log import configure_logger
from influxspeedtest.common.speedtest_cli_validation import check_for_speedtest_cli, attempt_to_install_speedtest_cli
from influxspeedtest.common.utils import run_speed_test, build_storage_handlers
from influxspeedtest.config.configmanager import ConfigManager

from influxspeedtest.storage.graphite.graphite_storage_handler import GraphiteStorageHandler


from influxspeedtest.storage.influxv1.influxv1_storage_handler import InfluxV1StorageHandler
from influxspeedtest.storage.influxv2.influxv2_storage_handler import InfluxV2StorageHandler

log = configure_logger(name=__name__)

config = ConfigManager(os.getenv('influxspeedtest', None) or 'config.ini')

if not check_for_speedtest_cli():
    log.error('Unable to find Speedtest CLI.  Attempting to install')
    try:
        attempt_to_install_speedtest_cli()
    except SpeedtestInstallFailure:
        sys.exit(1)
config.get_storage_configs()
build_storage_handlers(config)

# TODO - Dynamic loading based on config keys
storage_handlers = [
    InfluxV2StorageHandler('Influx v2', config),
    InfluxV1StorageHandler('Influx v1', config),
    GraphiteStorageHandler('Graphite', config)
]

while True:

    for server in config.servers:
        try:
            results = run_speed_test(server)
        except SpeedtestRunError:
            time.sleep(config.delay)
            continue

        log.debug(results)
        for handler in storage_handlers:
            if handler.active:
                handler.save_results(results)

    log.debug('Waiting %s seconds until next test', config.delay)
    time.sleep(config.delay)
