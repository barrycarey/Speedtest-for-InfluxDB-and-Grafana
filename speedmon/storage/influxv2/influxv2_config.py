from speedmon.storage.storage_config import StorageConfig


class InfluxV2Config(StorageConfig):
    name: str = 'Influx V2'
    url: str
    token: str
    org: str
    bucket: str
    verify_ssl: bool = False