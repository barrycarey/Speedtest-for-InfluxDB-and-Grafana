import os
from unittest import TestCase
from unittest.mock import patch

from influxspeedtest.common.utils import check_for_speedtest_cli


class Test(TestCase):

    @patch('influxspeedtest.common.utils.os_name')
    def check_for_speedtest_cli_windows(self, mock_os_name):
        os.mkdir(os.path.join(os.getcwd(), 'bin'))
        with open(os.path.join(os.getcwd(), 'bin', 'speedtest.exe')) as f:
            f.write('')
        mock_os_name.return_value = 'posix'

        r = check_for_speedtest_cli()

        print('')
