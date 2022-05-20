import os

from influxspeedtest.config.configmanager import ConfigManager

if os.getenv('influxspeedtest'):
    config = os.getenv('influxspeedtest')
else:
    config = 'config.ini'

config = ConfigManager(config)
