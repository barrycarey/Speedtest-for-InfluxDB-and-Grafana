import json
from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import patch, Mock

from speedmon.common.exceptions import SpeedtestRunError
from speedmon.common.speed_test_results import SpeedTestResult
from speedmon.common.utils import build_speedtest_command_line, run_speed_test


class Test(TestCase):

    @patch('speedmon.common.utils.os.getcwd')
    @patch('speedmon.common.utils.os_name')
    def test_build_speedtest_command_line_windows(self, mock_os_name, mock_getcwd):
        mock_getcwd.return_value = 'C:\\speedtest\\'
        mock_os_name.return_value = 'nt'
        expected = [r'C:\speedtest\bin\speedtest.exe', '-f', 'json']
        self.assertListEqual(expected, build_speedtest_command_line())

    @patch('speedmon.common.utils.os.getcwd')
    @patch('speedmon.common.utils.os_name')
    def test_build_speedtest_command_line_windows_with_server(self, mock_os_name, mock_getcwd):
        mock_getcwd.return_value = 'C:\\speedtest\\'
        mock_os_name.return_value = 'nt'
        expected = [r'C:\speedtest\bin\speedtest.exe', '-f', 'json', '-s', 1111]
        self.assertListEqual(expected, build_speedtest_command_line(server=1111))

    @patch('speedmon.common.utils.os_name')
    def test_build_speedtest_command_line_linux(self, mock_os_name):
        mock_os_name.return_value = 'posix'
        expected = [r'speedtest', '-f', 'json']
        self.assertListEqual(expected, build_speedtest_command_line())

    @patch('speedmon.common.utils.os_name')
    def test_build_speedtest_command_line_linux_with_server(self, mock_os_name):
        mock_os_name.return_value = 'posix'
        expected = [r'speedtest', '-f', 'json', '-s', 1111]
        self.assertListEqual(expected, build_speedtest_command_line(server=1111))

    @patch('speedmon.common.utils.subprocess.run')
    def test_run_speed_test_with_stderr(self, mock_subprocess):
        mock_subprocess.return_value = Mock(stderr='{"message": "some error"}')
        with self.assertRaises(SpeedtestRunError):
            run_speed_test()

    @patch('speedmon.common.utils.subprocess.run')
    def test_run_speed_test_with_stdout_error(self, mock_subprocess):
        mock_subprocess.return_value = Mock(stdout='{"error": "some error"}', stderr=None)
        with self.assertRaises(SpeedtestRunError):
            run_speed_test()

    @patch('speedmon.common.utils.subprocess.run')
    def test_run_speed_test_with_valid_results(self, mock_subprocess):
        results = {
            'ping': {
                'latency': 100
            },
            'download': {
                'bandwidth': 1000
            },
            'upload': {
                'bandwidth': 2000
            },
            'server': {
                'id': 1234,
                'name': 'test server',
                'country': 'USA',
                'location': 'Maine'
            }
        }
        mock_subprocess.return_value = Mock(stdout=json.dumps(results), stderr=None)
        r = run_speed_test()
        self.assertIsInstance(r, SpeedTestResult)
