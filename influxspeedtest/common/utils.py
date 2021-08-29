import json
import subprocess
from typing import Dict, List

from influxspeedtest.common.exceptions import SpeedtestRunError
from influxspeedtest.common.logging import log
from influxspeedtest.common.speed_test_results import SpeedTestResult



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

    proc_args = ['speedtest', '-f', 'json']
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

