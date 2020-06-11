FROM python:alpine

VOLUME /src/
COPY influxspeedtest.py requirements.txt /src/
ADD influxspeedtest /src/influxspeedtest
WORKDIR /src

RUN pip install -r requirements.txt

CMD ["python", "-u", "/src/influxspeedtest.py"]
