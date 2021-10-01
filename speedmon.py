import os
import sys
import time
from configparser import ConfigParser

from speedmon.common.exceptions import SpeedtestRunError, SpeedtestInstallFailure
from speedmon.common.logging.log import configure_logger
from speedmon.common.speedtest_cli_validation import check_for_speedtest_cli, attempt_to_install_speedtest_cli
from speedmon.common.utils import run_speed_test, save_results, run_speedtest_with_servers, \
    run_speedtest_with_default_server
from speedmon.config.config_manager import ConfigManager
from speedmon.storage.storage_builder import init_storage_handlers, \
    filter_dead_storage_handlers

log = configure_logger(name='speedmon')


if __name__ == '__main__':

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
        if servers:
            run_speedtest_with_servers(storage_handlers, servers)
        else:
            run_speedtest_with_default_server(storage_handlers)

        log.debug('Waiting %s seconds until next test', config.delay)
        time.sleep(config.delay)
