FROM python:3.3-slim
MAINTAINER Allan Tribe <atribe13@gmail.com>

VOLUME /src/config.ini
ADD . /src
WORKDIR /src

RUN pip install -r requirements.txt

CMD ["python", "/src/InfluxdbSpeedtest.py"]
