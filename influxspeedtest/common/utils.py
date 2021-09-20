import json
import logging
import os
import subprocess
from typing import Dict, List

from influxspeedtest.common.exceptions import SpeedtestRunError

from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.config.configmanager import ConfigManager
from influxspeedtest.storage.graphite.graphite_config import GraphiteConfig
from influxspeedtest.storage.graphite.graphite_storage_handler import GraphiteStorageHandler
from influxspeedtest.storage.influxv1.influxv1_config import InfluxV1Config
from influxspeedtest.storage.influxv1.influxv1_storage_handler import InfluxV1StorageHandler
from influxspeedtest.storage.influxv2.influxv2_config import InfluxV2Config
from influxspeedtest.storage.influxv2.influxv2_storage_handler import InfluxV2StorageHandler
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
    Wrapper around os.name to faciliate easier testing
    :rtype: str
    """
    return os.name


def build_storage_handlers(config_manager: ConfigManager) -> List[StorageHandlerBase]:
    handlers = []
    influx_v1_config = config_manager.get_influx_v1_settings()
    if influx_v1_config:
        handler = InfluxV1StorageHandler(InfluxV1Config(**influx_v1_config))
        if handler.active:
            handlers.append(handler)
    influx_v2_config = config_manager.get_influx_v2_settings()
    if influx_v1_config:
        handler = InfluxV2StorageHandler(InfluxV2Config(**influx_v2_config))
        if handler.active:
            handlers.append(handler)
    graphite_config = config_manager.get_graphite_settings()
    if influx_v1_config:
        handler = GraphiteStorageHandler(GraphiteConfig(**graphite_config))
        if handler.active:
            handlers.append(handler)
    return handlers
