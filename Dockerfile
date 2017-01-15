FROM python:3.3-slim
MAINTAINER Allan Tribe <atribe13@gmail.com>

VOLUME /src
ADD . /src

RUN pip install -r /src/requirements.txt

CMD ["python", "/src/InfluxdbSpeedtest.py"]
