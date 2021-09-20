import logging
from typing import Dict

from graphyte import Sender

from influxspeedtest.common.speed_test_results import SpeedTestResult
from influxspeedtest.storage.storage_handler_base import StorageHandlerBase


log = logging.getLogger(__name__)

class GraphiteStorageHandler(StorageHandlerBase):

    def _get_storage_client(self):
        return Sender(self.config.graphite_url, prefix=self.config.graphite_prefix, port=self.config.graphite_port, log_sends=True)

    def _validate_connection(self) -> None:
        try:
            self.client.send('health', 1)
            self.active = True
        except Exception as e:
            log.exception('Failed to activate graphite')
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
                'server_location': data.server_location.replace(' ', '_')
            }
        }