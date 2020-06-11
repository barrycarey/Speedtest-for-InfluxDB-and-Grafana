import configparser
import os
import sys


class ConfigManager():

    def __init__(self, config):

        self.servers = []
        config_file = os.path.join(os.getcwd(), config)
        if os.path.isfile(config_file):
            print('Loading Configuration File {}'.format(config))
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
            self._load_config_values()
        else:
            print(
                'No Configuration File {}\nGetting configuration from environment variables'.format(config))
            self._load_environment_values()

        print('Configuration Successfully Loaded')

    def _load_config_values(self):

        # InfluxDB
        self.influx_address = self.config['INFLUXDB']['Address']
        self.influx_port = self.config['INFLUXDB'].getint(
            'Port', fallback=8086)
        self.influx_database = self.config['INFLUXDB'].get(
            'Database', fallback='speedtests')
        self.influx_user = self.config['INFLUXDB'].get('Username', fallback='')
        self.influx_password = self.config['INFLUXDB'].get(
            'Password', fallback='')
        self.influx_ssl = self.config['INFLUXDB'].getboolean(
            'SSL', fallback=False)
        self.influx_verify_ssl = self.config['INFLUXDB'].getboolean(
            'Verify_SSL', fallback=True)

        # MQTT
        self.mqtt_hostname = self.config['MQTT']['Hostname']
        if self.mqtt_hostname:
            self.mqtt_port = self.config['MQTT'].getint('Port', fallback=1883)
            self.mqtt_user = self.config['MQTT'].get('Username', fallback='')
            self.mqtt_password = self.config['MQTT'].get(
                'Password', fallback='')
            self.mqtt_topicprefix = self.config['MQTT'].get(
                'Topic_Prefix', fallback='speedtest')

        # Logging
        self.logging_level = self.config['LOGGING'].get(
            'Level', fallback='debug')
        self.logging_level = self.logging_level.upper()

        # Speedtest
        test_server = self.config['SPEEDTEST'].get('Server', fallback=None)
        if test_server:
            self.servers = test_server.split(',')

    def _load_environment_values(self):
        self.influx_address = os.getenv('INFLUXDB_ADDRESS')
        self.influx_port = os.getenv('INFLUXDB_PORT') or 8086
        self.influx_port = int(self.influx_port)
        self.influx_database = os.getenv('INFLUXDB_DB') or "speedtests"
        self.influx_user = os.getenv('INFLUXDB_USER')
        self.influx_password = os.getenv('INFLUXDB_PASSWORD')
        self.influx_ssl = bool(os.getenv('INFLUXDB_SSL'))
        self.influx_verify_ssl = bool(os.getenv('INFLUXDB_VERIFYSSL'))

        # MQTT
        self.mqtt_hostname = os.getenv('MQTT_HOSTNAME')
        self.mqtt_port = os.getenv('MQTT_PORT') or 1883
        self.mqtt_port = int(self.mqtt_port)
        self.mqtt_user = os.getenv('MQTT_USERNAME') or "mqtt"
        self.mqtt_password = os.getenv('MQTT_PASSWORD') or "mqtt"
        self.mqtt_topicprefix = os.getenv('MQTT_PREFIX') or "speedtest"

        # Logging
        self.logging_level = os.getenv('LOGGING_LEVEL') or "debug"
        self.logging_level = self.logging_level.upper()

        # Speedtest
        test_server = os.getenv('SPEEDTEST_SERVERS') or None
        if test_server:
            self.servers = test_server.split(',')
