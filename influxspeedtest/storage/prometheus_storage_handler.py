from typing import Dict

from influxspeedtest.storage.storage_handler import StorageHandlerBase


class PrometheusStorageHandler(StorageHandlerBase):

    def __init__(self):
        raise NotImplementedError()
        self.client = self._get_storage_client()
        self._validate_connection()

    def _get_storage_client(self):
        pass

    def _validate_connection(self) -> None:
        pass

    def save_results(self, data: Dict):
        pass

    def format_results(self, data: Dict):
        pass