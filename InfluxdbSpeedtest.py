import configparser
import os
import sys
import argparse
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
import speedtest
import time

class configManager():

    def __init__(self, config):
        print('Loading Configuration File {}'.format(config))
        self.test_server = []
        config_file = os.path.join(os.getcwd(), config)
        if os.path.isfile(config_file):
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
        else:
            print('ERROR: Unable To Load Config File: {}'.format(config_file))
            sys.exit(1)

        self._load_config_values()
        print('Configuration Successfully Loaded')

    def _load_config_values(self):

        # General
        self.delay = self.config['GENERAL'].getint('Delay', fallback=2)
        self.output = self.config['GENERAL'].getboolean('Output', fallback=True)

        # InfluxDB
        self.influx_address = self.config['INFLUXDB']['Address']
        self.influx_port = self.config['INFLUXDB'].getint('Port', fallback=8086)
        self.influx_database = self.config['INFLUXDB'].get('Database', fallback='speedtests')
        self.influx_user = self.config['INFLUXDB'].get('Username', fallback='')
        self.influx_password = self.config['INFLUXDB'].get('Password', fallback='')
        self.influx_ssl = self.config['INFLUXDB'].getboolean('SSL', fallback=False)
        self.influx_verify_ssl = self.config['INFLUXDB'].getboolean('Verify_SSL', fallback=True)

        # Speedtest
        test_server = self.config['SPEEDTEST'].get('Server', fallback=None)
        if test_server:
            self.test_server.append(test_server)


class InfluxdbSpeedtest():

    def __init__(self, config=None):

        self.config = configManager(config=config)
        self.output = self.config.output
        self.influx_client = InfluxDBClient(
            self.config.influx_address,
            self.config.influx_port,
            username=self.config.influx_user,
            password=self.config.influx_password,
            database=self.config.influx_database,
            ssl=self.config.influx_ssl,
            verify_ssl=self.config.influx_verify_ssl
        )

        self.speedtest = None
        self.results = None
        self.setup_speedtest()

    def setup_speedtest(self):

        speedtest.build_user_agent()

        print('Getting speedtest.net Configuration')
        try:
            self.speedtest = speedtest.Speedtest()
        except speedtest.ConfigRetrievalError:
            print('ERROR: Failed to get speedtest.net configuration.  Aborting')
            sys.exit(1)

        try:
            self.speedtest.get_servers(self.config.test_server)
        except speedtest.NoMatchedServers:
            print('ERROR: No matched servers: {}'.format(self.config.test_server[0]))
            sys.exit(1)
        except speedtest.ServersRetrievalError:
            print('ERROR: Cannot retrieve speedtest server list')
            sys.exit(1)
        except speedtest.InvalidServerIDType:
            print('{} is an invalid server type, must be int'.format(self.config.test_server[0]))
            sys.exit(1)

        print('Picking the closest server')
        self.speedtest.get_best_server()

        self.results = self.speedtest.results

    def send_results(self):

        result_dict = self.results.dict()

        input_points = [
            {
                'measurement': 'speed_test_results',
                'fields': {
                    'download': result_dict['download'],
                    'upload': result_dict['upload'],
                    'ping': result_dict['server']['latency']
                },
                'tags': {
                    'server': result_dict['server']['sponsor']
                }
            }
        ]

        if self.output:
            print('Download: {}'.format(str(result_dict['download'])))
            print('Upload: {}'.format(str(result_dict['upload'])))

        self.write_influx_data(input_points)

    def run(self):

        while True:

            self.speedtest.download()
            self.speedtest.upload()

            self.send_results()

            time.sleep(self.config.delay)

    def write_influx_data(self, json_data):
        """
        Writes the provided JSON to the database
        :param json_data:
        :return:
        """
        if self.output:
            print(json_data)

        try:
            self.influx_client.write_points(json_data)
        except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
            if hasattr(e, 'code') and e.code == 404:

                print('Database {} Does Not Exist.  Attempting To Create'.format(self.config.influx_database))

                # TODO Grab exception here
                self.influx_client.create_database(self.config.influx_database)
                self.influx_client.write_points(json_data)

                return

            print('ERROR: Failed To Write To InfluxDB')
            print(e)

        if self.output:
            print('Written To Influx: {}'.format(json_data))


def main():

    parser = argparse.ArgumentParser(description="A tool to send Plex statistics to InfluxDB")
    parser.add_argument('--config', default='config.ini', dest='config', help='Specify a custom location for the config file')
    args = parser.parse_args()
    collector = InfluxdbSpeedtest(config=args.config)
    collector.run()


if __name__ == '__main__':
    main()
