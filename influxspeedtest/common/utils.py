import json
import logging
import os
import subprocess
from configparser import ConfigParser
from typing import Dict, List

from pydantic import ValidationError

from influxspeedtest.common.exceptions import SpeedtestRunError
from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.storage import storage_config_map
from influxspeedtest.storage.storage_handler_base import StorageHandlerBase

log = logging.getLogger(__name__)


def convert_results(results: Dict):
    return SpeedTestResult(
        results['ping']['jitter'] if 'jitter' in results['ping'] else None,
        results['ping']['latency'],
        results['download']['bandwidth'],
        results['upload']['bandwidth'],
        results['server']['id'],
        results['server']['name'],
        results['server']['country'],
        results['server']['location'])


def run_speed_test(server: int = None) -> SpeedTestResult:
    """
    Performs the speed test with the provided server
    :param server: Server to test against
    """
    if os_name() == 'nt':
        command = os.path.join(os.getcwd(), 'bin', 'speedtest.exe')
    else:
        command = 'speedtest'
    proc_args = [command, '-f', 'json']
    if server:
        proc_args += ['-s', server]

    log.debug('Running with args: %s', ' '.join(proc_args))
    process_result = subprocess.run(proc_args, capture_output=True, encoding='UTF-8')
    if process_result.stderr:
        error_data = json.loads(process_result.stderr)
        log.error('Failed to run speedtest: %s', error_data['message'])
        raise SpeedtestRunError(f'Failed to run speed test.  Message: {error_data["message"]}')

    results = json.loads(process_result.stdout)

    if 'error' in results:
        log.error('Problem running test: %s', results['error'])
        raise SpeedtestRunError(f'Failed to run speed test.  Message: {results["error"]}')

    return convert_results(results)


def os_name() -> str:
    """
    Wrapper around os.name to facilitate easier testing
    :rtype: str
    """
    return os.name


def filter_dead_storage_handlers(handler: StorageHandlerBase) -> bool:
    handler.validate_connection()
    return handler.active

def init_storage_handlers(config: ConfigParser) -> List[StorageHandlerBase]:
    """
    Create all storage handlers available in config file.
    :rtype: List[StorageHandlerBase]
    """
    handlers = []
    for section in config.sections():
        if 'storage' in section.lower():
            storage_handler_name = section.split('_')[1].lower()
            if storage_handler_name not in storage_config_map:
                log.error('Handler %s is not mapped, skipping', storage_handler_name)
                continue

            try:
                config = storage_config_map[storage_handler_name]['config'](**dict(config.items(section)))
            except ValidationError as e:
                log.error(e)
                continue
            handlers.append(
                storage_config_map[storage_handler_name]['handler'](config)
            )
            log.info('Storage Handler %s created', storage_handler_name)

    return list(filter(filter_dead_storage_handlers, handlers))

