import logging
from typing import Dict


from speedmon.common.speed_test_results import SpeedTestResult
from speedmon.storage.graphite.graphite_config import GraphiteConfig

from speedmon.storage.graphite.graphyte_sender import GraphyteSender
from speedmon.storage.storage_handler_base import StorageHandlerBase

log = logging.getLogger(__name__)


class GraphiteStorageHandler(StorageHandlerBase):

    def __init__(self, storage_config: GraphiteConfig):
        self.storage_config = storage_config
        super().__init__(storage_config)

    def _get_storage_client(self):
        return GraphyteSender(self.storage_config.url, prefix=self.storage_config.prefix, port=self.storage_config.port,
                      log_sends=True)

    def validate_connection(self) -> None:
        try:
            self.client.send('health', 1)
            self.active = True
        except ConnectionRefusedError as e:
            log.exception('Failed to activate graphite', exc_info=False)
            self.active = False

    def save_results(self, data: SpeedTestResult) -> None:
        formatted_results = self.format_results(data)
        for metric, value in formatted_results['metrics'].items():
            if not value:
                log.info('Dropping metric %s due to null value', metric)
                continue
            self.client.send(metric, value, tags=formatted_results['tags'])

    def format_results(self, data: SpeedTestResult) -> Dict:
        return {
            'metrics': {
                'latency': data.latency,
                'jitter': data.jitter,
                'download': data.download,
                'upload': data.upload,
                'packetloss': data.packetloss
            },
            'tags': {
                'server_id': data.server_id,
                'server_name': data.server_name.replace(' ', '_'),
                'server_country': data.server_country.replace(' ', '_'),
                'server_location': data.server_location.replace(', ', '_').replace(' ', '_')
            }
        }
