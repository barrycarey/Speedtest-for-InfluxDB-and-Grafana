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

Speedmon can be configured from a configuration file or environment variables.  The preferred method is via ENV.

### <a name="envvars"></a>Configuring From ENV

You only need to include the variables for the storage backends you wish to use. 

#### Influx v1

```
--Required--
INFLUXV1_URL
INFLUXV1_DATABASE_NAME
--Optional--
INFLUXV1_NAME
INFLUXV1_PORT
INFLUXV1_USER
INFLUXV1_PASSWORD
INFLUXV1_VERIFY_SSL
INFLUXV1_SSL
```

#### Influx v2

```
--Required--
INFLUXV2_URL
INFLUXV2_TOKEN
INFLUXV2_ORG
INFLUXV2_BUCKET

INFLUXV2_NAME
INFLUXV2_VERIFY_SSL
```

#### Graphite v2

```
--Required--
GRAPHITE_URL
GRAPHITE_PREFIX
--Optional--
GRAPHITE_NAME
GRAPHITE_PORT
```

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


## Usage

### With Docker (Preferred)

[See ENV Variable List For Your Storage Backend](#head1234)

```bash
docker run -d \
--name="speedtest" \
--restart="always" \
--env INFLUXV2_URL=http://example.com \
--env INFLUXV2_TOKEN=my-long-token \
--env INFLUXV2_ORG=my-org \
--env INFLUXV2_BUCKET=speedtests \
--env DELAY=360 \
barrycarey/speedmon:latest
```

#### Using Optional Configuration File 

If you do not want to configure Speedmon with ENV variables you can us configuration file

1. Make a directory to hold the config.ini file. Navigate to that directory and download the sample config.ini in this repo.
```bash
mkdir speedmon
curl -o speedmon/config.ini https://raw.githubusercontent.com/barrycarey/Speedmon/master/config.ini
cd speedmon
```
2. Modify the config file with your influxdb settings.
```bash
nano config.ini
```

Remove the unneeded storage backend sections.  Modify the remaining settings to fit our requirements

```buildoutcfg
[GENERAL]
Delay = 360
# Leave blank to auto pick server
Servers =


[INFLUXV2]
Name = Influx v2
URL = = http://localhost:8086
Token = abc12345676
Org = my-org
Bucket = speedtests
Verify_SSL = False


```

3. Run the container, pointing to the directory with the config file. This should now pull the image from Docker hub.

```bash
docker run -d \
--name="speedtest" \
-v config.ini:/src/config.ini \
--restart="always" \
--env SPEEDTEST_CONFIG=config.ini
barrycarey/speedmon:latest
```

Before the first use run pip3 install -r requirements.txt

Enter your desired information in config.ini 

Run influxspeedtest.py


## Adding Additional Backends
If you wish to contribute support for additional backends the process is straight forward. 

Add a new Package under ```speedmon.storage```.  Create a new Storage Handler that inherits from ```StorageHandlerBase```.  Create a new config that inherits from ```StorageConfig```.  Add the new storage backed to ```speedmon.storage.storage_config_map```

Add the example config options to config.ini and name the section ```[HANDLERNAME]```. This must match the name you specified in the map

The handler will automatically be loaded and initialized if the config options are available in the config.ini or ENV vars