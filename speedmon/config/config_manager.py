import configparser
import logging
import os
from typing import Dict, List

log = logging.getLogger(__name__)


class ConfigManager:

    def __init__(self, config_file=None, config_vals: Dict = None):
        self._default_delay = 360
        self._default_servers = []

        self.loaded_config = configparser.ConfigParser()

        if config_file:
            if os.path.isfile(config_file):
                log.info('Loading config from %s', config_file)
                self.loaded_config.read(config_file)
            elif not config_vals:
                raise ValueError('Provided config does not exist and no explicit config values defined')

        if config_vals:
            self.loaded_config.read_dict(config_vals)

        log.info('Configuration Successfully Loaded')


    @property
    def delay(self) -> int:
        if os.getenv('DELAY', None):
            return int(os.getenv('DELAY'))
        if 'GENERAL' in self.loaded_config:
            return self.loaded_config['GENERAL'].getint('Delay', fallback=60)
        return self._default_delay

    @property
    def servers(self) -> List:
        servers = None
        if 'GENERAL' not in self.loaded_config and not os.getenv('SERVERS', None):
            return self._default_servers
        if 'GENERAL' in self.loaded_config:
            servers = self.loaded_config['GENERAL'].get('Servers', fallback=None)
        if os.getenv('SERVERS', None):
            servers = os.getenv('SERVERS')

        if servers:
            return servers.split(',')

        return self._default_servers
