FROM python:3.3-slim
MAINTAINER Allan Tribe <atribe13@gmail.com>

VOLUME /src/
COPY influxspeedtest.py requirements.txt /src/
COPY config.ini /src/config.example.ini
ADD influxspeedtest /src/influxspeedtest
WORKDIR /src

RUN pip install -r requirements.txt

CMD ["python", "-u", "/src/influxspeedtest.py"]
