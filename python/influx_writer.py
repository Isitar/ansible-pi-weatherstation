from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxWriter:
    def __init__(self, token, org, bucket, url):
        client = InfluxDBClient(url=url, token=token)

        self.org = org
        self.bucket = bucket
        self.write_api = client.write_api(write_options=SYNCHRONOUS)

    def writeTemperature(self, sender, temperature):
        point = Point('temperature').tag('sender', sender).field('temperature', temperature)
        self.write_api.write(self.bucket, self.org, point)
    def writeHumidity(self, sender, humidity):
        point = Point('humidity').tag('sender', sender).field('humidity', humidity)
        self.write_api.write(self.bucket, self.org, point)
    def writePressure(self, sender, pressure):
        point = Point('pressure').tag('sender', sender).field('pressure', pressure)
        self.write_api.write(self.bucket, self.org, point)
    def writeLight(self, sender, light):
        point = Point('light').tag('sender', sender).field('light', light)
        self.write_api.write(self.bucket, self.org, point)