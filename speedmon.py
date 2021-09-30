import os
import sys
import time
from configparser import ConfigParser

from speedmon.common.exceptions import SpeedtestRunError, SpeedtestInstallFailure
from speedmon.common.logging.log import configure_logger
from speedmon.common.speedtest_cli_validation import check_for_speedtest_cli, attempt_to_install_speedtest_cli
from speedmon.common.utils import run_speed_test, save_results
from speedmon.config.config_manager import ConfigManager
from speedmon.storage.storage_builder import init_storage_handlers, \
    filter_dead_storage_handlers

log = configure_logger(name='speedmon')

def get_servers_env():
    if not os.getenv('SERVERS', None):
        return [None]


config = None
if os.getenv('SPEEDTEST_CONFIG', None):
    config = ConfigManager(config_file=os.getenv('SPEEDTEST_CONFIG'))


if not check_for_speedtest_cli():
    log.error('Unable to find Speedtest CLI.  Attempting to install')
    try:
        attempt_to_install_speedtest_cli()
    except SpeedtestInstallFailure:
        sys.exit(1)

if config:
    storage_handlers = init_storage_handlers(ini=config.loaded_config)
else:
    storage_handlers = init_storage_handlers()

storage_handlers = list(filter(filter_dead_storage_handlers, storage_handlers))

if not storage_handlers:
    log.error('No active storage handlers available ')

servers = []
while True:
    if not servers:
        try:
            results = run_speed_test()
        except SpeedtestRunError as e:
            log.error('Problem running speed test: %s', e)
            continue
        save_results(storage_handlers, results)

    for server in servers:
        try:
            results = run_speed_test(server)
        except SpeedtestRunError:
            time.sleep(config.delay)
            continue

        save_results(storage_handlers, results)

    log.debug('Waiting %s seconds until next test', config.delay)
    time.sleep(config.delay)

if __name__ == '__main__':
    pass