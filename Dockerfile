FROM python:3.12-alpine
LABEL maintainer="luis.ild@gmail.com"

ENV pin 17
ENV sleep 30
ENV port 8000

ENV PYTHONUNBUFFERED=1

WORKDIR /app
EXPOSE $port

RUN python3 -m venv /py 
RUN apk update && apk upgrade
RUN apk add g++ python3-dev git

RUN git clone https://github.com/luisgs/read_expose_dht_sensors.git /app
#COPY ./requirements.txt /app
#COPY ./DHT_rpi_sensor.py /app

RUN CFLAGS="-fcommon" /py/bin/pip install RPi.GPIO && \
#    apt update && \ 
#    apt install -y libsystemd0 libsystemd-dev && \ 
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install board && \
    /py/bin/pip install --upgrade setuptools && \
    /py/bin/pip install -r requirements.txt && \
    rm -rf /tmp && \
    apk del g++ python3-dev

# Execute command
CMD [ "sh", "-c", "/py/bin/python3 DHT_rpi_sensor.py $pin $sleep $port"]


