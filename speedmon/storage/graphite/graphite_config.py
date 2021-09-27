from speedmon.storage.storage_config import StorageConfig


class GraphiteConfig(StorageConfig):
    name: str = 'Graphite'
    url: str
    prefix: str = 'speedtest'
    port: int