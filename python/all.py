import time
# hardware
import pigpio
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
import board
# format & output
from datetime import datetime
import csv

# custom classes
import dht22_sensor
import bme280_sensor
import ldr_sensor

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
ldrsensor = ldr_sensor.sensor(board.SCK, board.MISO, board.MOSI, board.D26, 0)

with open('weather_data.csv', mode='a+') as data_file:
    data_writer = csv.writer(data_file, delimiter=';',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
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

        try:
            ldrsensor.trigger()
        except:
            print('ldr error')

        time.sleep(0.2)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        outputFormat = '{}: [{:10s}] {:7.2f}°C {:10.2f}hPa {:7.2f}% {:7d}'

        print(outputFormat.format(now, 'bme280', bme280sensor.temperature, bme280sensor.pressure, bme280sensor.humidity, 0))
        print(outputFormat.format(now, 'dht1', dht1.temperature(), 0, dht1.humidity(), 0))
        print(outputFormat.format(now, 'dht2', dht2.temperature(), 0, dht2.humidity(), 0))
        print(outputFormat.format(now, 'ldr', 0, 0, 0, ldrsensor.ldr_value))

        data_writer.writerow([now, 'bme280', bme280sensor.temperature,bme280sensor.pressure, bme280sensor.humidity, None])
        data_writer.writerow([now, 'dht1', dht1.temperature(), None, dht1.humidity(), None])
        data_writer.writerow([now, 'dht2', dht2.temperature(), None, dht2.humidity(), None])
        data_writer.writerow([now, 'ldr', None, None, None, ldrsensor.ldr_value])

        next_reading += INTERVAL

        # Overall INTERVAL second polling.
        time.sleep(next_reading-time.time())

dht1.cancel()
dht2.cancel()

pi.stop()
