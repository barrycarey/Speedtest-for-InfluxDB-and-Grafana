import os
from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import patch, Mock

from influxspeedtest.common.utils import init_storage_handlers
from influxspeedtest.storage import InfluxV1StorageHandler, InfluxV2StorageHandler


class Test(TestCase):

    def test_init_storage_handlers_no_configs(self):
        config = ConfigParser()
        config.read_dict({
            'GENERAL': {
                'timeout': 1
            }
        })
        self.assertEqual(0, len(init_storage_handlers(config)))

    def test_init_storage_handlers_not_mapped(self):
        config = ConfigParser()
        config.read_dict({
            'STORAGE_TEST': {
                'timeout': 1
            }
        })
        self.assertEqual(0, len(init_storage_handlers(config)))

    @patch('influxspeedtest.common.utils.filter_dead_storage_handlers')
    def test_init_storage_handlers_influxv1_init_valid_config(self, mock_init_handler):
        mock_init_handler.return_value = True
        config = ConfigParser()
        config.read_dict({
            'STORAGE_INFLUXV1': {
                'url': 'test',
                'port': '8086',
                'database': 'test',
                'username': 'test',
                'password': 'test',
                'ssl': 'false',
                'verify_ssl': 'false'
            }
        })
        result = init_storage_handlers(config)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], InfluxV1StorageHandler)

    @patch('influxspeedtest.common.utils.filter_dead_storage_handlers')
    def test_init_storage_handlers_influxv1_init_invalid_config(self, mock_init_handler):
        mock_init_handler.return_value = True
        config = ConfigParser()
        config.read_dict({
            'STORAGE_INFLUXV1': {

            }
        })
        result = init_storage_handlers(config)
        self.assertEqual(0, len(result))


    @patch('influxspeedtest.common.utils.filter_dead_storage_handlers')
    def test_init_storage_handlers_influxv2_init_valid_config(self, mock_init_handler):
        mock_init_handler.return_value = True
        config = ConfigParser()
        config.read_dict({
            'STORAGE_INFLUXV2': {
                'url': 'test',
                'token': 'test',
                'org': 'test',
                'bucket': 'test',
                'verify_ssl': 'false'
            }
        })
        result = init_storage_handlers(config)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], InfluxV2StorageHandler)

    @patch('influxspeedtest.common.utils.filter_dead_storage_handlers')
    def test_init_storage_handlers_influxv2_init_invalid_config(self, mock_init_handler):
        mock_init_handler.return_value = True
        config = ConfigParser()
        config.read_dict({
            'STORAGE_INFLUXV2': {

            }
        })
        result = init_storage_handlers(config)
        self.assertEqual(0, len(result))
