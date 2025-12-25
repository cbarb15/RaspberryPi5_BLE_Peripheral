import bluetooth_gatt
import bluetooth_constants
from LeftJoystickCharacteristic import  LeftJoystickCharacteristic
from RightJoystickCharacteristic import RightJoystickCharacteristic

class JoystickService(bluetooth_gatt.Service):
    def __init__(self, bus, path_base, index):
        print("Initialising JoystickService object")
        bluetooth_gatt.Service.__init__(self, bus, path_base, index,
        bluetooth_constants.JOYSTICK_SVC_UUID, True)
        print("Adding LeftJoystickCharacteristic to the service")
        self.add_characteristic(LeftJoystickCharacteristic(bus, 0, self))
        print("Adding RightJoystickCharacteristic to the service")
        self.add_characteristic(RightJoystickCharacteristic(bus, 1, self))
