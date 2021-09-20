import configparser
import os
import sys
from typing import Dict, Optional


class ConfigManager():

    def __init__(self, config_file, config_vals: Dict = None):
        print('Loading Configuration File {}'.format(config_file))
        self.servers = []
        config_file = os.path.join(os.getcwd(), config_file)
        self.config = configparser.ConfigParser()
        if not config_vals:
            if os.path.isfile(config_file):
                self.config.read(config_file)
            else:
                print('ERROR: Unable To Load Config File: {}'.format(config_file))
                sys.exit(1)
        else:
            self.config.read_dict(config_vals)

        self._load_config_values()
        print('Configuration Successfully Loaded')

    def _load_config_values(self):

        # General
        self.delay = self.config['GENERAL'].getint('Delay', fallback=2)


        # Speedtest
        servers = self.config['SPEEDTEST'].get('Servers', fallback=None)
        if servers:
            self.servers = servers.split(',')
        else:
            self.servers = [None]

    def get_storage_configs(self):
        for section in self.config.sections():
            pass

    def get_graphite_settings(self) -> Optional[Dict]:
        if not self.config.has_section('GRAPHITE'):
            return
        return {
            'name': self.config['GRAPHITE'].get('Name', fallback='Graphite'),
            'url': self.config['GRAPHITE'].get('URL', fallback=''),
            'prefix': self.config['GRAPHITE'].get('Prefix', fallback=''),
            'port': self.config['GRAPHITE'].getint('Port', fallback=2003)
        }

    def get_influx_v2_settings(self) -> Optional[Dict]:
        if not self.config.has_section('INFLUXV2'):
            return

        return {
            'name': self.config['INFLUXV2'].get('Name', fallback='Influx V2'),
            'url': self.config['INFLUXV2'].get('URL', fallback=''),
            'token': self.config['INFLUXV2'].get('Token', fallback=''),
            'org': self.config['INFLUXV2'].get('Org', fallback=''),
            'bucket': self.config['INFLUXV2'].get('Bucket', fallback=''),
            'ssl': self.config['INFLUXV2'].getboolean('Verify_SSL', fallback=True)
        }

    def get_influx_v1_settings(self) -> Optional[Dict]:
        if not self.config.has_section('INFLUXV1'):
            return
        return {
            'name': self.config['INFLUXV1'].get('Name', fallback='Influx V1'),
            'url': self.config['INFLUXV1']['Address'],
            'port': self.config['INFLUXV1'].getint('Port', fallback=8086),
            'database_name': self.config['INFLUXV1'].get('Database', fallback='speedtests'),
            'user': self.config['INFLUXV1'].get('Username', fallback=''),
            'password': self.config['INFLUXV1'].get('Password', fallback=''),
            'verify_ssl': self.config['INFLUXV1'].getboolean('Verify_SSL', fallback=True),
            'ssl': self.config['INFLUXV1'].getboolean('SSL', fallback=False)
        }