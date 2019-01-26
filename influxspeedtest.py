import argparse

from influxspeedtest.InfluxdbSpeedtest import InfluxdbSpeedtest

parser = argparse.ArgumentParser(description="A tool to take network speed test and send the results to InfluxDB")
args = parser.parse_args()
collector = InfluxdbSpeedtest()
collector.run()
