# Speedtest.net Collector For InfluxDB MQTT and Grafana


This tool is a wrapper for speedtest-cli which allows you to run periodic speedtets and save the results to Influxdb or MQTT (or neither)

## Configuration within config.ini

### INFLUXDB

| Key      | Description                                      |
|----------|--------------------------------------------------|
| Address  | InfluxDB Address                                 |
| Port     | InfluxDB port to connect to.  8086 in most cases |
| Database | Database to write collected stats to             |
| Username | User that has access to the database             |
| Password | Password for above user                          |

### MQTT

| Key          | Description                             |
|--------------|-----------------------------------------|
| Hostname     | MQTT Server Address                     |
| Port         | MQTT port to connect to.  Default: 1883 |
| Topic_Prefix | Prefix for the MQTT topic               |
| Username     | User that has access to the server      |
| Password     | Password for above user                 |

### SPEEDTEST

| Key    | Description                                           |
|--------|-------------------------------------------------------|
| Server | Comma sperated list of servers.  Leave blank for auto |

### LOGGING

| Key   | Description                           |
|-------|---------------------------------------|
| Level | Set how verbose the console output is |

## Configuration with Environment Variables

### INFLUXDB

| Key               | Description                                 |
|-------------------|---------------------------------------------|
| INFLUXDB_ADDRESS  | InfluxDB Address                            |
| INFLUXDB_PORT     | InfluxDB port to connect to.  Default: 8086 |
| INFLUXDB_DB       | Database to write collected stats to        |
| INFLUXDB_USER     | User that has access to the database        |
| INFLUXDB_PASSWORD | Password for above user                     |

### MQTT

| Key           | Description                             |
|---------------|-----------------------------------------|
| MQTT_HOSTNAME | MQTT Server Address                     |
| MQTT_PORT     | MQTT port to connect to.  Default: 1883 |
| MQTT_PREFIX   | Prefix for the MQTT topic               |
| MQTT_USERNAME | User that has access to the server      |
| MQTT_PASSWORD | Password for above user                 |

### SPEEDTEST

| Key               | Description                                           |
|-------------------|-------------------------------------------------------|
| SPEEDTEST_SERVERS | Comma sperated list of servers.  Leave blank for auto |

### LOGGING

| Key           | Description                           |
|---------------|---------------------------------------|
| LOGGING_LEVEL | Set how verbose the console output is |




## Usage

Before the first use run pip3 install -r requirements.txt

Enter your desired information in config.ini or set environment variables

Run influxspeedtest.py


