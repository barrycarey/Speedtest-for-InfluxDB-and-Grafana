import json
import logging
import os
import subprocess
from configparser import ConfigParser
from typing import Dict, List

from speedmon.common.exceptions import SpeedtestRunError
from speedmon.common.speed_test_results import SpeedTestResult
from speedmon.storage.storage_handler_base import StorageHandlerBase

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


def build_speedtest_command_line(server: int = None) -> List:
    if os_name() == 'nt':
        command = os.path.join(os.getcwd(), 'bin', 'speedtest.exe')
    else:
        command = 'speedtest'
    proc_args = [command, '-f', 'json']
    if server:
        proc_args += ['-s', server]
    return proc_args


def run_speed_test(server: int = None) -> SpeedTestResult:
    """
    Performs the speed test with the provided server
    :param server: Server to test against
    """

    proc_args = build_speedtest_command_line(server)
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


def save_results(storage_handlers: List[StorageHandlerBase], result: SpeedTestResult) -> None:
    for handler in storage_handlers:
        if handler.active:
            handler.save_results(result)