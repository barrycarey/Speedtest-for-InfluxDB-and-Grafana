from influxspeedtest.storage.graphite.graphite_config import GraphiteConfig
from influxspeedtest.storage.influxv1.influxv1_config import InfluxV1Config
from influxspeedtest.storage.influxv2.influxv2_config import InfluxV2Config

storage_config_map = {
    'influxv1': InfluxV1Config,
    'influxv2': InfluxV2Config,
    'graphite': GraphiteConfig
}