#!/usr/bin/env python3
import sys
import logging
import time

import Adafruit_DHT

from prometheus_client import Gauge, start_http_server
from systemd.journal import JournalHandler

# Setup logging to the Systemd Journal
log = logging.getLogger('dht22_sensor')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)


################
### Read DHT22 sensors at RPi and expose it via HTTP
################

##########
### Usage
### python3 script.py [argvs]
### python3 script.py PIN_OUT DHT_sensor_Description Readin_Interval TCP_port
###########

# Read args
n = len(sys.argv)
if (n != 5):
    print("Please insert valid arguments")
    print("dht_script PIN DHT_description Read_Interval Port")
    print("dht_script 4 INTERNAL 30 8000")
    exit()
else:
    PIN = int(sys.argv[1])  # 4 or 17
    DHT_description = sys.argv[2]
    read_interval = int(sys.argv[3])
    metrics_port = int(sys.argv[4])


# Initialize the DHT22 sensor
# Read data from GPIO4 pin on the Raspberry Pi
SENSOR = Adafruit_DHT.DHT22
SENSOR_PIN = PIN

# The time in seconds between sensor reads
READ_INTERVAL = read_interval 

# Create Prometheus gauges for humidity and temperature in
# Celsius and Fahrenheit
gh = Gauge('dht22_humidity_percent',
           'Humidity percentage measured by the DHT22 Sensor')
gt = Gauge('dht22_temperature',
           'Temperature measured by the DHT22 Sensor', ['scale'])

# Initialize the labels for the temperature scale
gt.labels('celsius')

# Variable that contains previous temp value,
# We initialize them
old_humidity, old_temperature = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN) 

while old_humidity is None and old_temperature is None:
    old_humidity, old_temperature = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN) 

def read_sensor():
    global old_humidity
    global old_temperature

    try:
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN)
    except RuntimeError as e:
        # GPIO access may require sudo permissions
        # Other RuntimeError exceptions may occur, but
        # are common.  Just try again.
        log.error("RuntimeError: {}".format(e))

    if (humidity is not None and temperature is not None and
            old_humidity is not None and old_temperature is not None):
        # Values are similar to previous ones
        if abs(humidity - old_humidity) < 5:
            gh.set(humidity)
            old_humidity = humidity
        else:
            gh.set(old_humidity)

        if abs(temperature - old_temperature) < 5:
            gt.labels('celsius').set(round(temperature, 2))
            old_temperature = temperature
        else:
            gt.labels('celsius').set(round(old_temperature, 2))
#       gt.labels('fahrenheit').set(celsius_to_fahrenheit(temperature))

        log.info("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%".format(temperature, humidity))

    time.sleep(READ_INTERVAL)

if __name__ == "__main__":

    # Expose metrics
    # metrics_port = 8000
    start_http_server(metrics_port)
    print("Serving " + DHT_description + " sensor metrics on :{}".format(metrics_port))
    log.info("Serving " + DHT_description + " sensor metrics on :{}".format(metrics_port))

    while True:
        read_sensor()
