#!/usr/bin/env python3
import sys
import logging
import time

import adafruit_dht 
import board

from prometheus_client import Gauge, start_http_server
from systemd.journal import JournalHandler

# Setup logging to the Systemd Journal
formatter = "%(asctime)s;%(levelname)s;%(message)s"
logging.basicConfig(format=formatter, stream=sys.stdout, level=logging.DEBUG)

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
SENSOR_PIN = PIN
SENSOR = adafruit_dht.DHT22(board.D17, use_pulseio=False)

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
try:
    old_humidity = SENSOR.humidity 
    old_temperature = SENSOR.temperature 
except RunTimeError as e:
    # GPIO access may require sudo permissions
    # Other RuntimeError exceptions may occur, but
    # are common.  Just try again.
    logging.error("RuntimeError: {}".format(e))
#while old_humidity is None and old_temperature is None:
#    old_humidity = SENSOR.humidity 
#    old_temperature = SENSOR.temperature 


def read_sensor():
    global old_humidity
    global old_temperature
    global SENSOR

    try:
        humidity = SENSOR.humidity 
        temperature = SENSOR.temperature 
        # logging.info("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%".format(temperature, humidity))
    except RuntimeError as e:
        # GPIO access may require sudo permissions
        # Other RuntimeError exceptions may occur, but
        # are common.  Just try again.
        logging.error("RuntimeError: {}".format(e))

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

        logging.info("Temp:{0:0.1f}*C, Humidity: {1:0.1f}%".format(temperature, humidity))

    logging.info("Going to sleep: " + str(READ_INTERVAL) + "s")
    time.sleep(READ_INTERVAL)

if __name__ == "__main__":

    # Expose metrics
    # metrics_port = 8000
    start_http_server(metrics_port)
    logging.info("Serving " + DHT_description + " sensor metrics on: {}".format(metrics_port))

    while True:
        try:
            read_sensor()
        except Exception as e:
            logging.error("Function has failed: {}".format(e))
