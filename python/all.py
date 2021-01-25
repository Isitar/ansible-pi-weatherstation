import time
import pigpio
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

import dht22_sensor
import bme280_sensor

# Intervals of about 2 seconds or less will eventually hang the DHT22.
INTERVAL = 3

pi = pigpio.pi()

dht1 = dht22_sensor.sensor(pi, 17, LED=22, power=27)
dht2 = dht22_sensor.sensor(pi, 5, LED=13, power=6)

r = 0

next_reading = time.time()
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
bme280sensor = bme280_sensor.sensor(bme280)

while True:
    r += 1

    try:
      dht1.trigger()
    except:
      dht1.rhum = 0
      dht1.temp = 0

    try:
      dht2.trigger()
    except:
      dht2.rhum = 0
      dht2.temp = 0

    try:
        bme280sensor.trigger()
    except:
      print('bme280 err')

    time.sleep(0.2)

   # print("{} {} {} {:3.2f} {} {} {} {}".format(
   #     r, s.humidity(), s.temperature(), s.staleness(),
   #     s.bad_checksum(), s.short_message(), s.missing_message(),
   #     s.sensor_resets()))

    print('{:4d}: [{:10s}] {:7.2f}°C {:10.2f}hPa {:7.2f}%'.format(r,'bme280', bme280sensor.temperature, bme280sensor.pressure, bme280sensor.humidity))
    print('{:4d}: [{:10s}] {:7.2f}°C {:10.2f}hPa {:7.2f}%'.format(r,'dht1', dht1.temperature(), 0, dht1.humidity()))
    print('{:4d}: [{:10s}] {:7.2f}°C {:10.2f}hPa {:7.2f}%'.format(r,'dht2', dht2.temperature(), 0, dht2.humidity()))

    next_reading += INTERVAL

    time.sleep(next_reading-time.time())  # Overall INTERVAL second polling.

s.cancel()

pi.stop()
