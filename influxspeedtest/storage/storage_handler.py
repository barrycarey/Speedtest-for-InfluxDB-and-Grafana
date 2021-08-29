from typing import Dict

from influxspeedtest.common.speed_test_results import SpeedTestResult


class StorageHandlerBase:

    def _get_storage_client(self):
        raise NotImplementedError()

    def _validate_connection(self) -> None:
        raise NotImplementedError()

    def save_results(self, data: SpeedTestResult) -> None:
        raise NotImplementedError()

    def format_results(self, data: SpeedTestResult) -> Dict:
        raise NotImplementedError()
