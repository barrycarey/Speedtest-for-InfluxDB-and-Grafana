from influxspeedtest.storage.storage_config import StorageConfig


class InfluxV1Config(StorageConfig):
    name: str = 'Influx V1'
    url: str
    port = 8086
    database_name = 'speedtests'
    user = ''
    password = ''
    verify_ssl = False
    ssl = False