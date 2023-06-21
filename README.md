# Exposing DHT22 sensor's value via HTTP for RPI

As the title indicates, this scripts expose in a TCP/IP port temperature and humidity values of a DHT22 sensor that is connected to your RPI.

It requires argvs:
> script.py DHT_PIN DHT_sensor_Description Readin_Interval TCP_port

For example, 
> script.py 7 DHT_1 30 8000

