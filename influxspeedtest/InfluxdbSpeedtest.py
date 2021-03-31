import sys
import time

import speedtest
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests import ConnectTimeout, ConnectionError

from influxspeedtest.common import log
from influxspeedtest.config import config


class InfluxdbSpeedtest():

    def __init__(self):

        self.influx_client = self._get_influx_connection()
        self.speedtest = None
        self.results = None

    def _get_influx_connection(self):
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

    def setup_speedtest(self, server=None):
        """
        Initializes the Speed Test client with the provided server
        :param server: Int
        :return: None
        """
        speedtest.build_user_agent()

        log.debug('Setting up SpeedTest.net client')

        if server is None:
            server = []
        else:
            server = server.split() # Single server to list

        try:
            self.speedtest = speedtest.Speedtest()
        except speedtest.ConfigRetrievalError:
            log.critical('Failed to get speedtest.net configuration.  Aborting')
            sys.exit(1)

        self.speedtest.get_servers(server)

        log.debug('Picking the closest server')

        self.speedtest.get_best_server()

        log.info('Selected Server %s in %s', self.speedtest.best['id'], self.speedtest.best['name'])

        self.results = self.speedtest.results

    def send_results(self):
        """
        Formats the payload to send to InfluxDB
        :rtype: None
        """
        result_dict = self.results.dict()

        input_points = [
            {
                'measurement': 'speed_test_results',
                'fields': {
                    'download': result_dict['download'],
                    'bytes_received': result_dict['bytes_received'],
                    'upload': result_dict['upload'],
                    'bytes_sent': result_dict['bytes_sent'],
                    'ping': result_dict['server']['latency'],
                    'isp': result_dict['client']['isp'],
                    'server': result_dict['server']['id'],
                    'server_name': result_dict['server']['name'],
                    'server_country': result_dict['server']['country'],
                    'server_sponsor': result_dict['server']['sponsor'],
                    'result_url': result_dict['share']
                },
                'tags': {
                    'server': result_dict['server']['id'],
                    'server_name': result_dict['server']['name'],
                    'server_country': result_dict['server']['country'],
                    'isp': result_dict['client']['isp']
                }
            }
        ]

        self.write_influx_data(input_points)

    def run_speed_test(self, server=None, share=False):
        """
        Performs the speed test with the provided server
        :param server: Server to test against
        """
        log.info('Starting Speed Test For Server %s', server)

        try:
            self.setup_speedtest(server)
        except speedtest.NoMatchedServers:
            log.error('No matched servers: %s', server)
            return
        except speedtest.ServersRetrievalError:
            log.critical('Cannot retrieve speedtest.net server list. Aborting')
            return
        except speedtest.InvalidServerIDType:
            log.error('%s is an invalid server type, must be int', server)
            return

        log.info('Starting download test')
        self.speedtest.download()
        log.info('Starting upload test')
        self.speedtest.upload()
        if(share):
            self.results.share()
        self.send_results()

        results = self.results.dict()
        log.info('Download: %sMbps - Upload: %sMbps - Latency: %sms - Share: %s',
                 round(results['download'] / 1000000, 2),
                 round(results['upload'] / 1000000, 2),
                 results['server']['latency'],
                 results['share']
                 )



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
            if not config.servers:
                self.run_speed_test(share=config.share)
            else:
                for server in config.servers:
                    self.run_speed_test(server, config.share)
            log.info('Waiting %s seconds until next test', config.delay)
            time.sleep(config.delay)
