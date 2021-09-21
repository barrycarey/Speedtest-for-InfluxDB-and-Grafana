from influxspeedtest.storage.graphite.graphite_config import GraphiteConfig
from influxspeedtest.storage.graphite.graphite_storage_handler import GraphiteStorageHandler
from influxspeedtest.storage.influxv1.influxv1_config import InfluxV1Config
from influxspeedtest.storage.influxv1.influxv1_storage_handler import InfluxV1StorageHandler
from influxspeedtest.storage.influxv2.influxv2_config import InfluxV2Config
from influxspeedtest.storage.influxv2.influxv2_storage_handler import InfluxV2StorageHandler

import logging

log = logging.getLogger(__name__)

storage_config_map = {
    'influxv1': {
        'config': InfluxV1Config,
        'handler': InfluxV1StorageHandler
    },
    'influxv2': {
        'config': InfluxV2Config,
        'handler': InfluxV2StorageHandler
    },
    'graphite': {
        'config': GraphiteConfig,
        'handler': GraphiteStorageHandler
    },

}