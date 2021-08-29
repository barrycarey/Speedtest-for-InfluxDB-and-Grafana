import json
import subprocess
import sys
import time
from typing import Dict, List

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectTimeout, ConnectionError

from influxspeedtest.common import log
from influxspeedtest.common.exceptions import SpeedtestRunError
from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.config import config


class InfluxdbSpeedtest():

    def __init__(self):

        self.influx_client = self._get_influx_connection()

    def _get_influx_connection(self) -> InfluxDBClient:
        """
        Create an InfluxDB connection and test to make sure it works.
        We test with the get all users command.  If the address is bad it fails
        with a 404.  If the user doesn't have permission it fails with 401
        :return:
        """

        influx = InfluxDBClient(
            config.influx_address,
            config.influx_port,
            database=config.influx_database,
            ssl=config.influx_ssl,
            verify_ssl=config.influx_verify_ssl,
            username=config.influx_user,
            password=config.influx_password,
            timeout=5
        )
        try:
            log.debug('Testing connection to InfluxDb using provided credentials')
            influx.get_list_users()  # TODO - Find better way to test connection and permissions
            log.debug('Successful connection to InfluxDb')
        except (ConnectTimeout, InfluxDBClientError, ConnectionError) as e:
            if isinstance(e, ConnectTimeout):
                log.critical('Unable to connect to InfluxDB at the provided address (%s)', config.influx_address)
            elif e.code == 401:
                log.critical('Unable to connect to InfluxDB with provided credentials')
            else:
                log.critical('Failed to connect to InfluxDB for unknown reason')

            sys.exit(1)

        return influx




    def write_influx_data(self, json_data):
        """
        Writes the provided JSON to the database
        :param json_data:
        :return: None
        """
        log.debug(json_data)

        try:
            self.influx_client.write_points(json_data)
        except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
            if hasattr(e, 'code') and e.code == 404:
                log.error('Database %s Does Not Exist.  Attempting To Create', config.influx_database)
                self.influx_client.create_database(config.influx_database)
                self.influx_client.write_points(json_data)
                return

            log.error('Failed To Write To InfluxDB')
            print(e)

        log.debug('Data written to InfluxDB')

    def run(self):

        while True:
            servers = config.servers
            if not servers:
                servers.append(None)
            for server in servers:
                try:
                    results = self.run_speed_test(server)
                except SpeedtestRunError:
                    time.sleep(config.delay)
                    continue

                log.debug(results)
                formatted_results = self.format_results_for_influxdb(results)
                self.write_influx_data(formatted_results)


            log.debug('Waiting %s seconds until next test', config.delay)
            time.sleep(config.delay)
