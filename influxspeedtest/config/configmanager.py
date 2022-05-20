import configparser
import os
import sys


class ConfigManager:

    def __init__(self, config):
        print('Loading Configuration File {}'.format(config))
        self.servers = []
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

        # InfluxDB
        self.influx_address = self.config['INFLUXDB']['Address']
        self.influx_port = self.config['INFLUXDB'].getint('Port', fallback=8086)
        self.influx_database = self.config['INFLUXDB'].get('Database', fallback='speedtests')
        self.influx_user = self.config['INFLUXDB'].get('Username', fallback='')
        self.influx_password = self.config['INFLUXDB'].get('Password', fallback='')
        self.influx_ssl = self.config['INFLUXDB'].getboolean('SSL', fallback=False)
        self.influx_verify_ssl = self.config['INFLUXDB'].getboolean('Verify_SSL', fallback=True)
        self.influx_retry_delay = self.config['INFLUXDB'].getint('Retry_Delay', 5)
        self.influx_retry_count = self.config['INFLUXDB'].getint('Retry_Count', 5)
        self.influx_retry_backoff = self.config['INFLUXDB'].getint('Backoff', 1)

        # Logging
        self.logging_level = self.config['LOGGING'].get('Level', fallback='debug')
        self.logging_level = self.logging_level.upper()

        # Speedtest
        test_server = self.config['SPEEDTEST'].get('Server', fallback=None)
        if test_server:
            self.servers = test_server.split(',')
