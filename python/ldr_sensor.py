import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class sensor:
    def __init__(self, clock, miso, mosi, digitalInOut, channel):
        # create the spi bus
        spi = busio.SPI(clock=clock, MISO=miso, MOSI=mosi)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(digitalInOut)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)
        # create an analog input channel on pin 0
        self.chan0 = AnalogIn(mcp, channel)
        self.ldr_value = 0

    def trigger(self):
        self.ldr_value = self.chan0.value
