import os
from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import patch

from pydantic import ValidationError

from speedmon.config.config_manager import ConfigManager
from speedmon.storage.graphite.graphite_config import GraphiteConfig
from speedmon.storage.graphite.graphite_storage_handler import GraphiteStorageHandler
from speedmon.storage.influxv1.influxv1_config import InfluxV1Config
from speedmon.storage.influxv1.influxv1_storage_handler import InfluxV1StorageHandler
from speedmon.storage.influxv2.influxv2_config import InfluxV2Config
from speedmon.storage.influxv2.influxv2_storage_handler import InfluxV2StorageHandler
from speedmon.storage.storage_builder import storage_handler_conf_from_env, \
    init_storage_handler_from_env, init_storage_handlers_from_env, \
    init_storage_handler_from_ini, init_storage_handlers_from_ini, storage_handler_config_from_ini, \
    storage_handler_name_in_env_vars
from speedmon.storage.storage_handler_base import StorageHandlerBase


class TestStorageBuilder(TestCase):


    def test_storage_handler_conf_from_env_influxv1(self):
        os.environ['INFLUXv1_NAME'] = 'influxv1 test'
        os.environ['INFLUXv1_URL'] = 'localhost'
        os.environ['INFLUXv1_PORT'] = '9999'
        os.environ['INFLUXv1_DATABASE_NAME'] = 'test_database'
        os.environ['INFLUXv1_USER'] = 'test_user'
        os.environ['INFLUXv1_PASSWORD'] = 'test_password'
        r = storage_handler_conf_from_env('influxv1')
        del os.environ['INFLUXv1_NAME']
        del os.environ['INFLUXv1_URL']
        del os.environ['INFLUXv1_PORT']
        del os.environ['INFLUXv1_DATABASE_NAME']
        del os.environ['INFLUXv1_USER']
        del os.environ['INFLUXv1_PASSWORD']
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

    def test_storage_handler_config_from_ini_odd_casing_value_names(self):
        ini = ConfigParser()
        ini.read_dict({
            'GRAPHITE': {
                'uRl': 'localhost'
            }
        })
        r = storage_handler_config_from_ini('graphite', ini)
        self.assertIsInstance(r, GraphiteConfig)

    def test_storage_handler_config_from_ini_invalid_handler_name(self):
        ini = ConfigParser()
        ini.read_dict({'GENERAL': {'Delay': 1}})
        with self.assertRaises(ValueError):
            storage_handler_config_from_ini('dummy_handler', ini)

    def test_storage_handler_config_from_ini_no_storage_settings(self):
        ini = ConfigParser()
        ini.read_dict({'GENERAL': {'Delay': 1}})
        with self.assertRaises(ValueError):
            storage_handler_config_from_ini('influxv2', ini)

    def test_storage_handler_config_from_ini_valid_config(self):
        ini = ConfigParser()
        ini.read_dict({'GRAPHITE': {
            'url': 'dummyhost'
        }})
        r = storage_handler_config_from_ini('graphite', ini)
        self.assertIsInstance(r, GraphiteConfig)
        self.assertEqual('dummyhost', r.url)

    def test_storage_handler_config_from_ini_missing_required(self):
        ini = ConfigParser()
        ini.read_dict({'GRAPHITE': {}})
        with self.assertRaises(ValidationError):
            storage_handler_config_from_ini('graphite', ini)

    def test_init_storage_handler_from_env_invalid_handler_name(self):
        self.assertIsNone(init_storage_handler_from_env('dummy'))

    def test_init_storage_handler_from_env_invalid_config(self):
        os.environ['GRAPHITE_PORT'] = '2003'
        r = init_storage_handler_from_env('graphite')
        del os.environ['GRAPHITE_PORT']
        self.assertIsNone(r)

    def test_init_storage_handler_from_env_valid_config(self):
        os.environ['GRAPHITE_URL'] = 'localhost'
        r = init_storage_handler_from_env('graphite')
        del os.environ['GRAPHITE_URL']
        self.assertIsInstance(r, StorageHandlerBase)
        self.assertIsInstance(r, GraphiteStorageHandler)

    def test_init_storage_handlers_from_env_invalid_config(self):
        r = init_storage_handlers_from_env()
        self.assertEqual(len(r), 0)

    def test_init_storage_handlers_from_env_invalid(self):
        os.environ['GRAPHITE_URL'] = 'localhost'
        r = init_storage_handlers_from_env()
        del os.environ['GRAPHITE_URL']
        self.assertEqual(len(r), 1)
        self.assertIsInstance(r[0], GraphiteStorageHandler)

    def test_init_storage_handlers_from_env_create_multiple(self):
        os.environ['GRAPHITE_URL'] = 'localhost'
        os.environ['INFLUXV2_URL'] = 'localhost'
        os.environ['INFLUXV2_TOKEN'] = 'abc'
        os.environ['INFLUXV2_ORG'] = 'test_org'
        os.environ['INFLUXV2_BUCKET'] = 'test_bucket'
        r = init_storage_handlers_from_env()
        del os.environ['GRAPHITE_URL']
        del os.environ['INFLUXV2_URL']
        del os.environ['INFLUXV2_TOKEN']
        del os.environ['INFLUXV2_ORG']
        del os.environ['INFLUXV2_BUCKET']
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[1], GraphiteStorageHandler)
        self.assertIsInstance(r[0], InfluxV2StorageHandler)

    def test_init_storage_handler_from_ini_invalid_handler_name(self):
        self.assertIsNone(init_storage_handler_from_ini('dummy', ConfigParser()))

    def test_init_storage_handler_from_ini_invalid_config(self):
        ini = ConfigParser()
        ini.read_dict({})
        r = init_storage_handler_from_ini('graphite', ini)
        self.assertIsNone(r)

    def test_init_storage_handler_from_ini_valid_config(self):
        ini = ConfigParser()
        ini.read_dict({
            'GRAPHITE': {
                'URL': 'localhost'
            }
        })
        r = init_storage_handler_from_ini('graphite', ini)
        self.assertIsInstance(r, StorageHandlerBase)
        self.assertIsInstance(r, GraphiteStorageHandler)

    def test_init_storage_handlers_from_ini_create_multiple(self):
        ini = ConfigParser()
        ini.read_dict({
            'GRAPHITE': {
                'URL': 'localhost'
            },
            'INFLUXV2': {
                'URL': 'localhost',
                'Token': 'abc',
                'Org': 'test_org',
                'Bucket': 'test_bucket'
            }
        })
        r = init_storage_handlers_from_ini(ini)
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[1], GraphiteStorageHandler)
        self.assertIsInstance(r[0], InfluxV2StorageHandler)

    def test_init_storage_handlers_from_ini_no_configs(self):
        ini = ConfigParser()
        ini.read_dict({
            'GENERAL': {
                'timeout': 1
            }
        })
        self.assertEqual(0, len(init_storage_handlers_from_ini(ini)))

    def test_storage_handler_name_in_env_vars_no(self):
        self.assertFalse(storage_handler_name_in_env_vars('influxv1'))

    def test_storage_handler_name_in_env_vars_yes(self):
        os.environ['INFLUXV1_URL'] = 'localhost'
        r = storage_handler_name_in_env_vars('influxv1')
        del os.environ['INFLUXV1_URL']
        self.assertTrue(r)