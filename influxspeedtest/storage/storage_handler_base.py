import logging
from typing import Dict, Text

from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.config import ConfigManager

log = logging.getLogger(__name__)


class StorageHandlerBase:

    def __init__(self, name: Text, config: ConfigManager):
        self.config = config
        self.active = False
        self.write_failures = 0
        self.name = name
        self.client = self._get_storage_client()
        self._validate_connection()
        if not self.active:
            log.error('Storage Handler %s failed to connect', self.name)
        else:
            log.info('Storage handler created and validated: %s', self.name)

    def _get_storage_client(self):
        """
        Build the client for the specific storage engine
        """
        raise NotImplementedError()

    def _validate_connection(self) -> None:
        """
        Validate we have an active connection to this storage client
        :rtype: None
        :return: None
        """
        raise NotImplementedError()

    def save_results(self, data: SpeedTestResult) -> None:
        """
        Save the speed test requests to this storage handler
        :rtype: SpeedTestResult
        :param data: Results data
        """
        raise NotImplementedError()

    def format_results(self, data: SpeedTestResult) -> Dict:
        """
        Format the generic speed test results for storage in this storage provider
        :param data: Speedtest data
        :rtype: Dict
        """
        raise NotImplementedError()
