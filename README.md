**Speedtest.net Collector For InfluxDB and Grafana**
------------------------------

This tool is a wrapper for speedtest-cli which allows you to run periodic speedtets and save the results to Influxdb 

## Configuration within config.ini

#### GENERAL
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Delay          |Delay between runs                                                                                                  |
|Output         |Write console output while tool is running                                                                          |
#### INFLUXDB
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Address        |Delay between updating metrics                                                                                      |
|Port           |InfluxDB port to connect to.  8086 in most cases                                                                    |
|Database       |Database to write collected stats to                                                                                |
|Username       |User that has access to the database                                                                                |
|Password       |Password for above user                                                                                             |
#### SPEEDTEST
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Server         |Server ID of speedtest.net server.  Leave blank for auto                                                            |



**Usage**

Before the first use run pip3 install -r requirements.txt

Enter your desired information in config.ini and run InfluxdbSpeedtest.py

Optionally, you can specify the --config argument to load the config file from a different location.  


***Requirements***

Python 3+

You will need the influxdb library installed to use this - [Found Here](https://github.com/influxdata/influxdb-python)
You will need the speedtest-cli library installed to use this - [Found Here](https://github.com/sivel/speedtest-cli)

