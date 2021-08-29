import configparser
import os
import sys


class ConfigManager():

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

        # Influx v1
        self.influx_v1_address = self.config['INFLUXV1']['Address']
        self.influx_v1_port = self.config['INFLUXV1'].getint('Port', fallback=8086)
        self.influx_v1_database = self.config['INFLUXV1'].get('Database', fallback='speedtests')
        self.influx_v1_user = self.config['INFLUXV1'].get('Username', fallback='')
        self.influx_v1_password = self.config['INFLUXV1'].get('Password', fallback='')
        self.influx_v1_ssl = self.config['INFLUXV1'].getboolean('SSL', fallback=False)
        self.influx_v1_verify_ssl = self.config['INFLUXV1'].getboolean('Verify_SSL', fallback=True)

        # INFLUX v2
        self.influx_v2_url = self.config['INFLUXV2'].get('URL', fallback='')
        self.influx_v2_token = self.config['INFLUXV2'].get('Token', fallback='')
        self.influx_v2_org = self.config['INFLUXV2'].get('Org', fallback='')
        self.influx_v2_bucket = self.config['INFLUXV2'].get('Bucket', fallback='')

        # Logging
        self.log_level = self.config['LOGGING'].get('Level', fallback='debug')
        self.log_level = self.log_level.upper()

        # Speedtest
        servers = self.config['SPEEDTEST'].get('Servers', fallback=None)
        if servers:
            self.servers = servers.split(',')
        else:
            self.servers = [None]
