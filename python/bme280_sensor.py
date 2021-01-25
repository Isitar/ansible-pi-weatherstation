class sensor:
    def __init__(self, bme280):
        self.bme280 = bme280
        self.temperature = 0
        self.pressure = 0
        self.humidity = 0

    def trigger(self):
        self.temperature = self.bme280.get_temperature()
        self.pressure = self.bme280.get_pressure()
        self.humidity = self.bme280.get_humidity()
