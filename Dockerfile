FROM python:alpine
MAINTAINER Barry Carey <mcarey66@gmail.com>

VOLUME /src/
COPY influxspeedtest.py requirements.txt config.ini /src/
ADD influxspeedtest /src/influxspeedtest
WORKDIR /src
ENV RUN_ENV=docker
ENV LOG_LEVEL=INFO
RUN pip install -r requirements.txt

CMD ["python", "-u", "/src/influxspeedtest.py"]
