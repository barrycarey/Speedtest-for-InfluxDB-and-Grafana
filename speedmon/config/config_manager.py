import configparser
import logging
import os
from typing import Dict, List

log = logging.getLogger(__name__)


class ConfigManager:

    def __init__(self, config_file=None, config_vals: Dict = None):
        if not config_file and not config_vals:
            raise ValueError('Please provide either a config file or config values')

        if config_file and config_vals:
            log.error('Config file and values provided.  Only config file will be used')

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
        return self.loaded_config['GENERAL'].getint('Delay', fallback=60)

    @property
    def servers(self) -> List:
        if os.getenv('SERVERS', None):
            servers = os.getenv('SERVERS')
        else:
            servers = self.loaded_config['GENERAL'].get('Servers', fallback=None)

        if servers:
            return servers.split(',')

        # TODO - This is hacky.  Mainly to keep logic clean in speedmon.py.  Forces speed test to run with no server set
        return [None]
