from typing import Dict

from influxdb_client import InfluxDBClient
from influxspeedtest.common import log
from influxspeedtest.common.exceptions import StorageHandlerFailure
from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.config import config
from influxspeedtest.storage.storage_handler import StorageHandlerBase


class InfluxV2StorageHandler(StorageHandlerBase):

    def _get_storage_client(self):
        return InfluxDBClient(
            url=config.influx_v2_url,
            token=config.influx_v2_token,
            org=config.influx_v2_org,
        )

    def _validate_connection(self):
        health = self.client.health()
        if health.status == 'fail':
            log.critical('Failed to connect to InfluxDB v2: %s', health.message)
            raise StorageHandlerFailure('Failed to connect to storage engine')
        self.active = True


    def save_results(self, data: SpeedTestResult) -> None:
        with self.client.write_api() as _write_client:
            _write_client.write(config.influx_v2_bucket, config.influx_v2_org, self.format_results(data))

    def format_results(self, data: SpeedTestResult) -> Dict:
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