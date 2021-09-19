import os
import shutil
from unittest import TestCase
from unittest.mock import patch, Mock

from influxspeedtest.common.exceptions import UnsupportedOperatingSystem
from influxspeedtest.common.speedtest_cli_validation import check_for_speedtest_cli_windows, check_for_speedtest_cli, \
    check_for_speedtest_cli_linux


class Test(TestCase):
    def test_check_for_speedtest_cli_windows_binary_exists_return_true(self):
        os.mkdir(os.path.join(os.getcwd(), 'bin'))
        with open(os.path.join(os.getcwd(), 'bin', 'speedtest.exe'), 'w') as f:
            f.write('')
        result = check_for_speedtest_cli_windows()
        shutil.rmtree(os.path.join(os.getcwd(), 'bin'))
        self.assertTrue(result)

    def test_check_for_speedtest_cli_windows_binary_not_exist_return_false(self):
        self.assertFalse(check_for_speedtest_cli_windows())

    def test_check_for_speedtest_cli_in_docker_check(self):
        os.environ['RUN_ENV'] = 'docker'
        self.assertTrue(check_for_speedtest_cli())

    def test_check_for_speedtest_cli_not_in_docker(self):
        self.assertFalse(check_for_speedtest_cli())

    @patch('influxspeedtest.common.speedtest_cli_validation.os_name')
    def test_check_for_speedtest_cli_unsupported_raise(self, mock_os_name):
        mock_os_name.return_value = 'junk'
        with self.assertRaises(UnsupportedOperatingSystem):
            check_for_speedtest_cli()

    @patch('influxspeedtest.common.speedtest_cli_validation.os_name')
    @patch('influxspeedtest.common.speedtest_cli_validation.check_for_speedtest_cli_windows')
    def test_check_for_speedtest_cli_windows_call(self, mock_win_check, mock_os_name):
        mock_os_name.return_value = 'nt'
        check_for_speedtest_cli()
        self.assertTrue(mock_win_check.called)

    @patch('influxspeedtest.common.speedtest_cli_validation.os_name')
    @patch('influxspeedtest.common.speedtest_cli_validation.check_for_speedtest_cli_linux')
    def test_check_for_speedtest_cli_linux_call(self, mock_linux_check, mock_os_name):
        mock_os_name.return_value = 'posix'
        check_for_speedtest_cli()
        self.assertTrue(mock_linux_check.called)

    @patch('influxspeedtest.common.speedtest_cli_validation.subprocess.run')
    def test_check_for_speedtest_cli_linux_installed(self, mock_run):
        res_mock = Mock(stdout='/bin/speedtest')
        mock_run.return_value = res_mock
        self.assertTrue(check_for_speedtest_cli_linux())

    @patch('influxspeedtest.common.speedtest_cli_validation.subprocess.run')
    def test_check_for_speedtest_cli_linux_not_installed(self, mock_run):
        res_mock = Mock(stdout='')
        mock_run.return_value = res_mock
        self.assertFalse(check_for_speedtest_cli_linux())