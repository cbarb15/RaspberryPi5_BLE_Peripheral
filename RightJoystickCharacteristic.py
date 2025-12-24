import bluetooth_gatt
import bluetooth_constants
import dbus
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
from adafruit_extended_bus import ExtendedI2C as I2C

class RightJoystickCharacteristic(bluetooth_gatt.Characteristic):
    def __init__(self, bus, index, service):
        bluetooth_gatt.Characteristic.__init__(
        self, bus, index,
        bluetooth_constants.JOYSTICK_RIGHT_Y_VALUE_CHR_UUID, ['read','notify'], service)
        self.notifying = False
        self.i2c = I2C(3)
        self.ads = ADS1115(self.i2c)
        self.right_joystick = AnalogIn(self.ads, ads1x15.Pin.A1)


    def ReadValue(self, options):
        print("ReadValue in RightJoystickCharacteristic Called")
        print("Returning "+str(self.right_joystick.value))
        value = self.right_joystick.value.to_bytes(2, "big")

        return value