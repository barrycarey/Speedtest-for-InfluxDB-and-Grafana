FROM python:3.9.7-slim-bullseye
MAINTAINER Barry Carey <mcarey66@gmail.com>

VOLUME /src/
COPY speedmon.py requirements.txt config.ini /src/
ADD speedmon /src/speedmon
WORKDIR /src
ENV RUN_ENV=docker
ENV LOG_LEVEL=INFO
RUN apt-get update && apt-get install -y curl && curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash && apt-get install speedtest -y  && pip install -r requirements.txt --no-cache-dir

CMD ["python", "-u", "/src/speedmon.py"]
