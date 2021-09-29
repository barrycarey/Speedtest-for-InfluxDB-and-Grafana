import os
import sys
import time

from speedmon.common.exceptions import SpeedtestRunError, SpeedtestInstallFailure
from speedmon.common.logging.log import configure_logger
from speedmon.common.speedtest_cli_validation import check_for_speedtest_cli, attempt_to_install_speedtest_cli
from speedmon.common.utils import run_speed_test
from speedmon.config.config_manager import ConfigManager
from speedmon.storage.storage_builder import init_storage_handlers, \
    filter_dead_storage_handlers

log = configure_logger(name='speedmon')

config = None
if os.getenv('SPEEDTEST_CONFIG', None):
    config = ConfigManager(config_file=os.getenv('SPEEDTEST_CONFIG'))



if not check_for_speedtest_cli():
    log.error('Unable to find Speedtest CLI.  Attempting to install')
    try:
        attempt_to_install_speedtest_cli()
    except SpeedtestInstallFailure:
        sys.exit(1)


storage_handlers = init_storage_handlers(ini=config.loaded_config)
storage_handlers = list(filter(filter_dead_storage_handlers, storage_handlers))

if not storage_handlers:
    log.error('No active storage handlers available ')

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
