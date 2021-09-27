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

Settings are loaded from the config.ini in the root of the project.  

If you wish to override the config location, set the SPEEDTEST_CONFIG environment variable with the path to the file

Storage backends are dynamically loaded based on what is in the config file. You can safely delete the sections for backends not in use.  

#### GENERAL
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Delay          |Delay between runs                                                                                                  |
#### STORAGE_INFLUXV1
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Url            |URL of InfluxDB server                                                                                     |
|Port           |InfluxDB port to connect to.  8086 in most cases                                                                    |
|Database       |Database to write collected stats to                                                                                |
|Username       |User that has access to the database                                                                                |
|Password       |Password for above user                                                                                             |
|SSL       | Use SSL Connection                                                                                        |
|Verify SSL       |Validate SSL cert    
#### STORAGE_INFLUXV2
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Url            |URL of InfluxDB server                                                                                     |
|Token       | API token to use                                                                                |
|Bucket       |Bucket to user                                                                                            |
|Org       | Org to use                                                                                        |
|Verify SSL       |Validate SSL cert  |
#### STORAGE_GRAPHITE
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Url            |URL of Graphite server                                                                                     |
|Prefix       | Metric Prefix                                                                               |
|Port       | Graphite Port                                                                                          |
#### SPEEDTEST
|Key            |Description                                                                                                         |
|:--------------|:-------------------------------------------------------------------------------------------------------------------|
|Server         |Comma sperated list of servers.  Leave blank for auto                                                            |



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