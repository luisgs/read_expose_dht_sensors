# Exposing DHT22 sensor's value via HTTP for RPI

As the title indicates, this script exposes via HTTP both temperature and humidity values of a DHT22 sensor that is connected to your RPI.

Exposing values via HTTP allows us to read values from prometheus/Grafana for future tracking and monitoring reasons.

It requires argvs:
> script.py DHT_PIN DHT_sensor_Description Readin_Interval TCP_port

For example, 
> script.py 7 DHT_1 30 8000

This repository includes an output for better clarification. 
