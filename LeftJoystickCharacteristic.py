import bluetooth_gatt
import bluetooth_constants
import dbus
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
from adafruit_extended_bus import ExtendedI2C as I2C

class LeftJoystickCharacteristic(bluetooth_gatt.Characteristic):
    def __init__(self, bus, index, service):
        bluetooth_gatt.Characteristic.__init__(
        self, bus, index,
        bluetooth_constants.JOYSTICK_LEFT_Y_VALUE_CHR_UUID, ['read','notify'], service)
        self.notifying = False
        self.i2c = I2C(3)
        self.ads = ADS1115(self.i2c)
        self.left_joystick = AnalogIn(self.ads, ads1x15.Pin.A0)


    def ReadValue(self, options):
        print("ReadValue in JoystickCharacteristic Called")
        print("Returning "+str(self.left_joystick.value))
        value = self.left_joystick.value.to_bytes(2, "big")

        return value