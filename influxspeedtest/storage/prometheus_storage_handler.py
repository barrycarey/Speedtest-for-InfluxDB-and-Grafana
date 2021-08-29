from typing import Dict

from influxspeedtest.storage.storage_handler import StorageHandlerBase


class PrometheusStorageHandler(StorageHandlerBase):

    def __init__(self):
        pass

    def save_results(self, data: Dict):
        pass

    def format_results(self, data: Dict):
        pass