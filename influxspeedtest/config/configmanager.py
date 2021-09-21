import configparser
import logging
import os
import sys
from typing import Dict, Optional


log = logging.getLogger(__name__)

class ConfigManager():

    def __init__(self, config_file, config_vals: Dict = None):
        log.info('Loading Configuration File %s', config_file)
        self.servers = []
        config_file = os.path.join(os.getcwd(), config_file)
        self.loaded_config = configparser.ConfigParser()
        if not config_vals:
            if os.path.isfile(config_file):
                self.loaded_config.read(config_file)
            else:
                log.error('ERROR: Unable To Load Config File: %s', config_file)
                sys.exit(1)
        else:
            self.loaded_config.read_dict(config_vals)

        self._load_config_values()
        log.info('Configuration Successfully Loaded')

    def _load_config_values(self):

        # General
        self.delay = self.loaded_config['GENERAL'].getint('Delay', fallback=2)

        # Speedtest
        servers = self.loaded_config['SPEEDTEST'].get('Servers', fallback=None)
        if servers:
            self.servers = servers.split(',')
        else:
            self.servers = [None]

