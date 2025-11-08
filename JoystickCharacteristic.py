import bluetooth_gatt
import bluetooth_constants
import dbus
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_extended_bus import ExtendedI2C as I2C

class JoystickCharacteristic(bluetooth_gatt.Characteristic):
    def __init__(self, bus, index, service):
        bluetooth_gatt.Characteristic.__init__(
        self, bus, index,
        bluetooth_constants.JOYSTICK_LEFT_Y_VALUE_CHR_UUID, ['read','notify'], service)
        self.notifying = False
        self.i2c = I2C(3)
        self.ads = ADS.ADS1115(self.i2c)
        self.left_joystick = AnalogIn(self.ads, ADS.P0)


    def ReadValue(self, options):
        print("ReadValue in JoystickCharacteristic Called")
        print("Returning "+str(self.left_joystick.value))
        # value = []
        # value.append(dbus.Byte(self.left_joystick.value))
        value = self.left_joystick.value.to_bytes(2, "big")

        return value