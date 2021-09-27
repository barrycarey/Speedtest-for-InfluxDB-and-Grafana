import logging
from typing import Dict, List

from influxdb_client import InfluxDBClient

from speedmon.common.speed_test_results import SpeedTestResult
from speedmon.storage.influxv2.influxv2_config import InfluxV2Config

from speedmon.storage.storage_handler_base import StorageHandlerBase

log = logging.getLogger(__name__)


class InfluxV2StorageHandler(StorageHandlerBase):

    def __init__(self, storage_config: InfluxV2Config):
        self.storage_config = storage_config
        super().__init__(storage_config)

    def _get_storage_client(self):
        return InfluxDBClient(
            url=self.storage_config.url,
            token=self.storage_config.token,
            org=self.storage_config.org,
        )

    def validate_connection(self):
        health = self.client.health()
        if health.status == 'fail':
            log.error('Failed to connect to InfluxDB v2: %s', health.message)
            self.active = False
            return
        self.active = True


    def save_results(self, data: SpeedTestResult) -> None:
        with self.client.write_api() as _write_client:
            _write_client.write(self.storage_config.bucket, self.storage_config.org, self.format_results(data))

    def format_results(self, data: SpeedTestResult) -> List[Dict]:
        input_points = [
            {
                'measurement': 'speed_test_results',
                'fields': {
                    'download': data.download,
                    'upload': data.upload,
                    'ping': data.latency,
                    'jitter': data.jitter,
                    'packetloss': data.packetloss,
                },
                'tags': {
                    'server_id': data.server_id,
                    'server_name': data.server_name,
                    'server_country': data.server_country,
                    'server_location': data.server_location
                }
            }
        ]
        return input_points