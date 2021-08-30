import sys
from typing import Dict

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectTimeout, ConnectionError

from influxspeedtest.common.exceptions import StorageHandlerFailure
from influxspeedtest.common.logging import log
from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.config import config
from influxspeedtest.storage.storage_handler import StorageHandlerBase


class InfluxV1StorageHandler(StorageHandlerBase):

    def _get_storage_client(self):
        return InfluxDBClient(
            config.influx_v1_address,
            config.influx_v1_port,
            database=config.influx_v1_database,
            ssl=config.influx_v1_ssl,
            verify_ssl=config.influx_v1_verify_ssl,
            username=config.influx_v1_user,
            password=config.influx_v1_password,
            timeout=5
        )

    def _validate_connection(self):
        try:
            log.debug('Testing connection to InfluxDb using provided credentials')
            self.client.get_list_users()  # TODO - Find better way to test connection and permissions
            log.debug('Successful connection to InfluxDb')
        except (ConnectTimeout, InfluxDBClientError, ConnectionError) as e:
            if isinstance(e, ConnectTimeout):
                log.critical('Unable to connect to InfluxDB at the provided address (%s)', config.influx_v1_address)
            elif e.code == 401:
                log.critical('Unable to connect to InfluxDB with provided credentials')
            else:
                log.critical('Failed to connect to InfluxDB for unknown reason')
            return

        self.active = True


    def save_results(self, data: SpeedTestResult):

        try:
            self.client.write_points(self.format_results(data))
            self.write_failures = 0
        except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
            if hasattr(e, 'code') and e.code == 404:
                log.error('Database %s Does Not Exist.  Attempting To Create', config.influx_v1_database)
                self.client.create_database(config.influx_v1_database)
                self.client.write_points(self.format_results(data))
                return

            self.write_failures += 1
            log.exception('Failed To Write To InfluxDB', exc_info=True)
            return

        log.debug('Data written to Influx DB V1')

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