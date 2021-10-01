**SpeedMon**
------------------------------

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/barrycarey/redditrepostsleuth)
![Master](https://github.com/barrycarey/RedditRepostSleuth/workflows/Tests/badge.svg)
![Travis (.com)](https://img.shields.io/travis/com/barrycarey/RedditRepostSleuth)
![semver](https://img.shields.io/badge/semver-1.0.0-blue)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/barrycarey/RedditRepostSleuth/master)
------------------------------
![Screenshot](https://puu.sh/tmfOA/b5576e88de.png)
------------------------------
Automatically run periodic internet speed tests and save results to a variety of storage backends.  

**Supported Backends**
* InfluxDB v1
* InfluxDB v2
* Graphite

Speed tests are run using the official speedtest.net CLI tool. 

Docker, Windows, and Linux are supported.  Linux users are required to install the speedtest package first. It will automatically download on Windows. 

## Configuration

Speedmon can be configured from a configuration file or environment variables.  

### Configuring From .ini

When initializing Speedmon looks for the SPEEDTEST_CONFIG ENV Variable to know what config file to load.  If this variable 
is not provided, Speedmon will attempt to load settings from ENV.

Storage backends are dynamically loaded based on what is in the config file. You can safely delete the sections for backends not in use.  

```buildoutcfg
[INFLUXV1]
Name = Whatever You want
Url = http://localhost
Port = 8086
User = 
Password =
SSL = False
Verify SSL = False
```

```buildoutcfg
[INFLUXV2]
Name = Whatever You want
Url = http://localhost
Token =
Org = 
Bucket = 
Verify SSL = False
```

```buildoutcfg
[Graphite]
Name = Whatever You want
Url = http://localhost
Port = 2003
Prefix = speedtest
```

### Configuring From ENV

#### Influx v1

```
INFLUXV1_NAME
INFLUXV1_URL
INFLUXV1_PORT
INFLUXV1_DATABASE_NAME
INFLUXV1_USER
INFLUXV1_PASSWORD
INFLUXV1_VERIFY_SSL
INFLUXV1_SSL
```

#### Influx v2

```
INFLUXV2_NAME
INFLUXV2_URL
INFLUXV2_TOKEN
INFLUXV2_ORG
INFLUXV2_BUCKET
INFLUXV2_VERIFY_SSL
```

#### Graphite v2

```
GRAPHITE_NAME
GRAPHITE_URL
GRAPHITE_PREFIX
GRAPHITE_PORT

```
## Usage

Before the first use run pip3 install -r requirements.txt

Enter your desired information in config.ini 

Run influxspeedtest.py

**Custom Config File Name**

If you wish to use a config file by a different name set an ENV Variable called influxspeedtest.  The value you set will be the config file that's used. 
  

***Requirements***

Python 3+

You will need the influxdb library installed to use this - [Found Here](https://github.com/influxdata/influxdb-python)
You will need the speedtest-cli library installed to use this - [Found Here](https://github.com/sivel/speedtest-cli)

## Docker Setup

1. Install [Docker](https://www.docker.com/)

2. Make a directory to hold the config.ini file. Navigate to that directory and download the sample config.ini in this repo.
```bash
mkdir speedtest
curl -o speedtest/config.ini https://raw.githubusercontent.com/barrycarey/Speedtest-for-InfluxDB-and-Grafana/master/config.ini
cd speedtest
```

3. Modify the config file with your influxdb settings.
```bash
nano config.ini
```
Modify the 'Address =' line include the ip or hostname of your influxdb instance.
Example:
```bash
Address = 10.13.14.200
```

4. Run the container, pointing to the directory with the config file. This should now pull the image from Docker hub. You can do this by either running docker run or by using docker-compose.
 1. The docker run option.
```bash
docker run -d \
--name="speedtest" \
-v config.ini:/src/config.ini \
--restart="always" \
barrycarey/speedtest-for-influxdb-and-grafana
```
 2. The docker-compose option
 ```bash
 curl -O https://raw.githubusercontent.com/barrycarey/Speedtest-for-InfluxDB-and-Grafana/master/docker-compose.yml docker-compose.yml
 docker-compose up -d
 ```

## Adding Additional Backends
If you wish to contribute support for additional backends the process is straight forward. 

Add a new Package under speedmon.storage.  Create a new Storage Handler that inherits from StorageHandlerBase.  Create a new config that inherits from StorageConfig.  Add the new storage backed to speedmon.storage.storage_config_map

Add the example config options to config.ini and name the section [STORAGE_NAME].  

The handler will automatically be loaded and initialized if the config options are available in the config.ini