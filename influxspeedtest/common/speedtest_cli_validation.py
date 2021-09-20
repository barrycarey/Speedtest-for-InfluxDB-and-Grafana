import logging
import os
import subprocess
import sys
import zipfile
from io import BytesIO

import requests

from influxspeedtest.common.exceptions import UnsupportedOperatingSystem, SpeedtestInstallFailure
from influxspeedtest.common.utils import os_name

log = logging.getLogger(__name__)

def check_for_speedtest_cli() -> bool:
    if os.getenv('RUN_ENV', None) == 'docker':
        return True
    if os_name() == 'nt':
        return check_for_speedtest_cli_windows()
    elif os_name() == 'posix':
        check_for_speedtest_cli_linux()
    else:
        raise UnsupportedOperatingSystem(f'Unsupported OS {os_name()}')

def check_for_speedtest_cli_windows() -> bool:
    if os.path.isfile(os.path.join(os.getcwd(), 'bin', 'speedtest.exe')):
        return True
    return False

def check_for_speedtest_cli_linux() -> bool:
    res = subprocess.run(['which', 'speedtest'], capture_output=True, encoding='UTF-8')
    if not res.stdout:
        return False
    return True

def attempt_to_install_speedtest_cli():
    if os_name() != 'nt':
        log.error('Automatic install is not supported on your OS. Please follow installation instructions here https://www.speedtest.net/apps/cli')
        raise UnsupportedOperatingSystem(f'Unsupported OS {os_name()}')
    download_speedtest_cli_windows()


def download_speedtest_cli_windows():
    r = requests.get('https://install.speedtest.net/app/cli/ookla-speedtest-1.0.0-win64.zip')
    if r.status_code != 200:
        log.critical('Unable to download Speedtest CLI package, aborting')
        raise SpeedtestInstallFailure('Failed to download Speedtest CLI')

    # TODO - Need error handling
    zfile = zipfile.ZipFile(BytesIO(r.content))
    bin_dir = os.path.join(os.getcwd(), 'bin')
    if not os.path.isdir(bin_dir):
        os.mkdir(bin_dir)
    zfile.extractall(bin_dir)
    if not os.path.isfile(os.path.join(bin_dir, 'speedtest.exe')):
        log.critical('Failed to download Speedtest CLI executable')
        raise SpeedtestInstallFailure('Failed to download Speedtest CLI')
