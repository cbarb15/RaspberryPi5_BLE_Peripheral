import bluetooth_constants
import bluetooth_exceptions
import dbus
import dbus.exceptions
import dbus.service
import dbus.mainloop.glib
import sys
from gi.repository import GLib
sys.path.insert(0, '.')
from Advertisement import Advertisement
from JoystickApplication import JoystickApplication
import board
import busio
import digitalio

bus = None
adapter_path = None
adv_mgr_interface = None

def register_ad_cb():
    print('Advertisement registered OK')

def register_ad_error_cb(error):
    print('Error: Failed to register advertisement: ' + str(error))
    mainloop.quit()

def set_connected_status(status):
   global connected
   if status == 1:
      print("Connected")
      connected = 1
      stop_advertising()
   else:
      print("Disconnected")
      connected = 0
      start_advertising()

def properties_changed(interface, changed, invalidated, path):
   if interface == bluetooth_constants.DEVICE_INTERFACE:
      if "Connected" in changed:
         set_connected_status(changed["Connected"])
      
def interfaces_added(path, interfaces):
   if bluetooth_constants.DEVICE_INTERFACE in interfaces:
      properties = interfaces[bluetooth_constants.DEVICE_INTERFACE]
      if "Connected" in properties:
         set_connected_status(properties["Connected"])

def stop_advertising():
   global adv
   global adv_mgr_interface
   print("Unregistering advertisement",adv.get_path())
   adv_mgr_interface.UnregisterAdvertisement(adv.get_path())

def start_advertising():
    global adv
    global adv_mgr_interface
    # we're only registering one advertisement object so index (arg2) is hard coded as 0
    print("Registering advertisement",adv.get_path())
    adv_mgr_interface.RegisterAdvertisement(adv.get_path(), {},
                                        reply_handler=register_ad_cb,
                                        error_handler=register_ad_error_cb)
    
def register_app_cb():
   print("GATT application registered")

def register_app_error_cb(error):
   print("Failed to register application: " + str(error))
   mainloop.quit()

if __name__ == '__main__':
   while(1):
      print("Running.....")
      cs = digitalio.DigitalInOut(board.D22)
      cs.direction = digitalio.Direction.OUTPUT
      cs.value = True
      spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

      while not spi.try_lock():
         pass

      spi.configure(baudrate=5000000, phase=0, polarity=0)
      cs.value = False
      spi.write(bytes([0x01, 0xFF]))
      cs.value = True
      
   # dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
   # bus = dbus.SystemBus()
   # # we're assuming the adapter supports advertising
   # adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + bluetooth_constants.ADAPTER_NAME
   # print(adapter_path)

   # bus.add_signal_receiver(properties_changed, dbus_interface = bluetooth_constants.DBUS_PROPERTIES, signal_name = "PropertiesChanged", path_keyword = "path")
   # bus.add_signal_receiver(interfaces_added, dbus_interface = bluetooth_constants.DBUS_OM_IFACE, signal_name = "InterfacesAdded")

   # adv_mgr_interface = dbus.Interface(bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME,adapter_path), bluetooth_constants.ADVERTISING_MANAGER_INTERFACE)
   # # we're only registering one advertisement object so index (arg2) is hard coded as 0
   # adv = Advertisement(bus, 0, 'peripheral')
   # start_advertising()

   # print("Advertising as "+adv.local_name)

   # mainloop = GLib.MainLoop()

   # app = JoystickApplication(bus)
   # print('Registering GATT application...')
   # service_manager = dbus.Interface(
   # bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME,
   # adapter_path),
   # bluetooth_constants.GATT_MANAGER_INTERFACE)
   # service_manager.RegisterApplication(app.get_path(), {}, reply_handler=register_app_cb, error_handler=register_app_error_cb)
                                       
   # mainloop.run()
