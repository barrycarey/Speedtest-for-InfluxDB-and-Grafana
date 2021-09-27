from enum import Enum

from speedmon.storage.graphite.graphite_config import GraphiteConfig
from speedmon.storage.graphite.graphite_storage_handler import GraphiteStorageHandler
from speedmon.storage.influxv1.influxv1_config import InfluxV1Config
from speedmon.storage.influxv1.influxv1_storage_handler import InfluxV1StorageHandler
from speedmon.storage.influxv2.influxv2_config import InfluxV2Config
from speedmon.storage.influxv2.influxv2_storage_handler import InfluxV2StorageHandler

STORAGE_CONFIG_MAP = {
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

storage_env_map = {
    'influxv1': [
        'INFLUXV1_NAME',
        'INFLUXV1_URL',
        'INFLUXV1_PORT',
        'INFLUXV1_DATABASE',
        'INFLUXV1_USERNAME',
        'INFLUXV1_PASSWORD',
        'INFLUXV1_SSL',
        'INFLUXV1_VERIFY_SSL'
    ],
    'influxv2': [
        'INFLUXv2_'
    ]
}

class ValidHandlerNames(Enum):
    InfluxV1 = 'influxv1'
    Influxv2 = 'influxv2'
    Graphite = 'graphite'