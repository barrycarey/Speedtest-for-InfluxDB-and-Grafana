import os
from unittest import TestCase

from speedmon.config.config_manager import ConfigManager


class TestConfigManager(TestCase):

    def test_init_invalid_config_file_and_no_vals(self):
        with self.assertRaises(ValueError):
            ConfigManager(config_file='dummyfile.ini')

    def test_servers_no_config_or_env_val(self):
        config = ConfigManager(config_vals={'GENERAL': {}})
        self.assertListEqual([], config.servers)

    def test_servers_valid_values(self):
        config = ConfigManager(config_vals={'GENERAL': {'Servers': '1234,5678'}})
        self.assertListEqual(['1234', '5678'], config.servers)

    def test_servers_valid_values_from_env(self):
        os.environ['SERVERS'] = '9876,5432'
        config = ConfigManager(config_vals={'GENERAL': {'Servers': '1234,5678'}})
        self.assertListEqual(['9876', '5432'], config.servers)
        del os.environ['SERVERS']

    def test_delay_no_set_value(self):
        config = ConfigManager(config_vals={'GENERAL': {}})
        self.assertEqual(60, config.delay)

    def test_delay_value_from_cfg(self):
        config = ConfigManager(config_vals={'GENERAL': {'Delay': 55}})
        self.assertEqual(55, config.delay)

    def test_delay_value_from_env(self):
        os.environ['DELAY'] = '42'
        config = ConfigManager(config_vals={'GENERAL': {'Delay': 55}})
        self.assertEqual(42, config.delay)
        del os.environ['DELAY']

    def test_delay_no_cfg_or_env(self):
        config = ConfigManager(config_vals={'DUMMY': {}})
        self.assertEqual(360, config.delay)