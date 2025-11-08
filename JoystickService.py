import bluetooth_gatt
import bluetooth_constants
from JoystickCharacteristic import  JoystickCharacteristic


class JoystickService(bluetooth_gatt.Service):
    def __init__(self, bus, path_base, index):
        print("Initialising JoystickService object")
        bluetooth_gatt.Service.__init__(self, bus, path_base, index,
        bluetooth_constants.JOYSTICK_SVC_UUID, True)
        print("Adding JoystickCharacteristic to the service")
        self.add_characteristic(JoystickCharacteristic(bus, 0, self))