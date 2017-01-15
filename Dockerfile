FROM python:3.3-slim
MAINTAINER Allan Tribe <atribe13@gmail.com>

VOLUME /src
ADD . /src

CMD ["python", "/src/InfluxdbSpeedtest.py"]
