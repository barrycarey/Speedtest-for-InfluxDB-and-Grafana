FROM python:3.3-slim
MAINTAINER Allan Tribe <atribe13@gmail.com>

VOLUME /src/
COPY InfluxdbSpeedtest.py requirements.txt /src/
WORKDIR /src

RUN pip install -r requirements.txt

CMD ["python", "-u", "/src/InfluxdbSpeedtest.py"]
