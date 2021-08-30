from typing import Dict

from graphyte import Sender

from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.config import config
from influxspeedtest.storage.storage_handler import StorageHandlerBase


class GraphiteStorageHandler(StorageHandlerBase):

    def _get_storage_client(self):
        return Sender(config.graphite_url, port=config.graphite_port)

    def _validate_connection(self) -> None:
        self.client.send('speedtest.health', 1)

    def save_results(self, data: SpeedTestResult) -> None:
        pass

    def format_results(self, data: SpeedTestResult) -> Dict:
        pass