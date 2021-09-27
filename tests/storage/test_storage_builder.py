import os
from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import patch

from pydantic import ValidationError

from speedmon.storage.constants import ValidHandlerNames
from speedmon.storage.graphite.graphite_config import GraphiteConfig
from speedmon.storage.influxv1.influxv1_config import InfluxV1Config
from speedmon.storage.influxv1.influxv1_storage_handler import InfluxV1StorageHandler
from speedmon.storage.influxv2.influxv2_config import InfluxV2Config
from speedmon.storage.influxv2.influxv2_storage_handler import InfluxV2StorageHandler
from speedmon.storage.storage_builder import init_storage_handlers_from_cfg, storage_handler_conf_from_env


class TestStorageBuilder(TestCase):

    def test_init_storage_handlers_no_configs(self):
        config = ConfigParser()
        config.read_dict({
            'GENERAL': {
                'timeout': 1
            }
        })
        self.assertEqual(0, len(init_storage_handlers_from_cfg(config)))

    def test_init_storage_handlers_not_mapped(self):
        config = ConfigParser()
        config.read_dict({
            'STORAGE_TEST': {
                'timeout': 1
            }
        })
        self.assertEqual(0, len(init_storage_handlers_from_cfg(config)))

    @patch('speedmon.storage.storage_builder.filter_dead_storage_handlers')
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
        result = init_storage_handlers_from_cfg(config)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], InfluxV1StorageHandler)

    @patch('speedmon.storage.storage_builder.filter_dead_storage_handlers')
    def test_init_storage_handlers_influxv1_init_invalid_config(self, mock_init_handler):
        mock_init_handler.return_value = True
        config = ConfigParser()
        config.read_dict({
            'STORAGE_INFLUXV1': {

            }
        })
        result = init_storage_handlers_from_cfg(config)
        self.assertEqual(0, len(result))


    @patch('speedmon.storage.storage_builder.filter_dead_storage_handlers')
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
        result = init_storage_handlers_from_cfg(config)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], InfluxV2StorageHandler)

    @patch('speedmon.storage.storage_builder.filter_dead_storage_handlers')
    def test_init_storage_handlers_influxv2_init_invalid_config(self, mock_init_handler):
        mock_init_handler.return_value = True
        config = ConfigParser()
        config.read_dict({
            'STORAGE_INFLUXV2': {

            }
        })
        result = init_storage_handlers_from_cfg(config)
        self.assertEqual(0, len(result))

    def test_storage_handler_conf_from_env_influxv1(self):
        os.environ['INFLUXv1_NAME'] = 'influxv1 test'
        os.environ['INFLUXv1_URL'] = 'localhost'
        os.environ['INFLUXv1_PORT'] = '9999'
        os.environ['INFLUXv1_DATABASE_NAME'] = 'test_database'
        os.environ['INFLUXv1_USER'] = 'test_user'
        os.environ['INFLUXv1_PASSWORD'] = 'test_password'
        r = storage_handler_conf_from_env('influxv1')
        self.assertIsInstance(r, InfluxV1Config)
        self.assertEqual(r.user, 'test_user')
        self.assertEqual(r.password, 'test_password')
        self.assertEqual(r.name, 'influxv1 test')
        self.assertEqual(r.url, 'localhost')
        self.assertEqual(r.database_name, 'test_database')

    def test_storage_handler_conf_from_env_influxv2(self):
        os.environ['INFLUXv2_NAME'] = 'influxv2 test'
        os.environ['INFLUXv2_URL'] = 'localhost'
        os.environ['INFLUXv2_TOKEN'] = 'abc123'
        os.environ['INFLUXv2_ORG'] = 'test_org'
        os.environ['INFLUXv2_BUCKET'] = 'test_bucket'
        r = storage_handler_conf_from_env('influxv2')
        self.assertIsInstance(r, InfluxV2Config)
        self.assertEqual(r.token, 'abc123')
        self.assertEqual(r.org, 'test_org')
        self.assertEqual(r.bucket, 'test_bucket')
        self.assertEqual(r.name, 'influxv2 test')
        self.assertEqual(r.url, 'localhost')

    def test_storage_handler_conf_from_env_graphite(self):
        os.environ['GRAPHITE_NAME'] = 'graphite test'
        os.environ['GRAPHITE_URL'] = 'localhost'
        os.environ['GRAPHITE_PREFIX'] = 'testprefix'
        os.environ['GRAPHITE_PORT'] = '2003'

        r = storage_handler_conf_from_env('graphite')
        self.assertIsInstance(r, GraphiteConfig)
        self.assertEqual(r.prefix, 'testprefix')
        self.assertEqual(r.port, 2003)
        self.assertEqual(r.name, 'graphite test')
        self.assertEqual(r.url, 'localhost')


    def test_storage_handler_conf_from_env_influxv1_missing_required(self):
        if 'INFLUXv1_URL' in os.environ:
            del os.environ['INFLUXv1_URL']
        with self.assertRaises(ValidationError):
            storage_handler_conf_from_env('influxv1')

    def test_storage_handler_conf_from_env_invalid_handler_name(self):
        with self.assertRaises(ValueError):
            storage_handler_conf_from_env('dummy_handler')

