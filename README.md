# Read DHT22 values and exposes them via HTTP

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/luisgs/read_expose_dht_sensors.git)

As the title indicates, this is a python script that  exposes via HTTP both temperature and humidity values of a DHT22 sensor that is connected to your RPI's GPIO pins.

Final goal is to read these values from Prometheus or Grafana for real tracking, monitoring and archiving reasons.

## Tech

Read DHT22 sensors currently uses these technologies:

- Python
- Adafruit DHT
- Prometheus Client [Gauge, start_http_server]

## Use

Here is how to execute this script:

```sh
[sudo] python3 DHT_rpi_sensor.py [GPIO_port] [INTERVAL_seconds] [TCP_port]
```

```sh
[sudo] python3 DHT_rpi_sensor.py 17 30 8000
```

## Docker

Read DHT22 sensor is very easy to install and deploy in a Docker container.

You can find a dockerfile in here

By default, the Docker will expose port 8000, so change this within the
Dockerfile if necessary or during executition of the docker itself (compose). When ready, simply use the Dockerfile to
build the image.

More info in the link above.

```sh
sudo docker build -t dockerfile_dht22 .
sudo docker run --privileged -v /sys:/sys -e pin=17 -e sleep=30 -dp 0.0.0.0:8040:8000 dockerfile_dht22
```
