import logging
from typing import Dict, List

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectTimeout, ConnectionError, InvalidURL

from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.storage.influxv1.influxv1_config import InfluxV1Config
from influxspeedtest.storage.storage_handler_base import StorageHandlerBase

log = logging.getLogger(__name__)


class InfluxV1StorageHandler(StorageHandlerBase):

    def __init__(self, storage_config: InfluxV1Config):
        self.storage_config = storage_config
        super().__init__(storage_config)

    def _get_storage_client(self):
        return InfluxDBClient(
            self.storage_config.url,
            self.storage_config.port,
            database=self.storage_config.database_name,
            ssl=self.storage_config.ssl,
            verify_ssl=self.storage_config.verify_ssl,
            username=self.storage_config.user,
            password=self.storage_config.password,
            timeout=5
        )

    def _validate_connection(self):
        try:
            log.debug('Testing connection to InfluxDb using provided credentials')
            self.client.get_list_users()  # TODO - Find better way to test connection and permissions
            log.debug('Successful connection to InfluxDb')
            self.active = True
        except (ConnectTimeout, InfluxDBClientError, ConnectionError, InvalidURL) as e:
            if isinstance(e, InvalidURL):
                log.error('Invalid URL for Influx V1')
            elif isinstance(e, ConnectTimeout):
                log.error('Unable to connect to InfluxDB at the provided address (%s)', self.config.influx_v1_address)
            elif e.code == 401:
                log.error('Unable to connect to InfluxDB with provided credentials')
            else:
                log.error('Failed to connect to InfluxDB for unknown reason')
            self.active = False
            return

        self.active = True

    def save_results(self, data: SpeedTestResult):

        try:
            self.client.write_points(self.format_results(data))
            self.write_failures = 0
        except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
            if hasattr(e, 'code') and e.code == 404:
                log.error('Database %s Does Not Exist.  Attempting To Create', self.storage_config.database_name)
                self.client.create_database(self.storage_config.database_name)
                self.client.write_points(self.format_results(data))
                return

            self.write_failures += 1
            log.exception('Failed To Write To InfluxDB', exc_info=True)
            return

        log.debug('Data written to Influx DB V1')

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
