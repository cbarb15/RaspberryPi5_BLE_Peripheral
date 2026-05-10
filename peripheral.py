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
import serial
import digitalio
import time
import multiprocessing
import gpiod
from gpiod.line import Direction, Value, Bias, Edge
from gpiod.line_settings import LineSettings
import select
from datetime import timedelta
import os
from BatteryMonitor import BatteryMonitor
import struct

SHUTDOWN_THRESHOLD = 3  # Number of consecutive failures required for shutdown
SLEEP_TIME = 60  # Time in seconds to wait between failure checks
MONITOR_INTERVAL = 3  # Seconds between monitoring checks

bus = None
adapter_path = None
uart_process = None
mainloop = None
chip_path = "/dev/gpiochip0"

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

def start_advertising_and_create_GATT_app():
   global adv
   global adv_mgr_interface
   dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
   bus = dbus.SystemBus()
   adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + bluetooth_constants.ADAPTER_NAME
   print(adapter_path)

   bus.add_signal_receiver(properties_changed, dbus_interface = bluetooth_constants.DBUS_PROPERTIES, signal_name = "PropertiesChanged", path_keyword = "path")
   bus.add_signal_receiver(interfaces_added, dbus_interface = bluetooth_constants.DBUS_OM_IFACE, signal_name = "InterfacesAdded")

   adv_mgr_interface = dbus.Interface(bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME,adapter_path), bluetooth_constants.ADVERTISING_MANAGER_INTERFACE)
   # we're only registering one advertisement object so index (arg2) is hard coded as 0
   adv = Advertisement(bus, 0, 'peripheral')
   start_advertising()

   print("Advertising as "+adv.local_name)

   mainloop = GLib.MainLoop()

   app = JoystickApplication(bus)
   print('Registering GATT application...')
   service_manager = dbus.Interface(
   bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME,
   adapter_path),
   bluetooth_constants.GATT_MANAGER_INTERFACE)
   service_manager.RegisterApplication(app.get_path(), {}, reply_handler=register_app_cb, error_handler=register_app_error_cb)

   mainloop.run()

def battery_monitor_task():
   global battery_line_request
   global uart
   battery_monitor = BatteryMonitor(battery_line_request)

   print(f"battery monitor request {battery_monitor.request}")
   failure_counter = 0

   while True:
      # Read GPIO value
      values = battery_monitor.request.get_values()

      ac_power_state = values[battery_monitor.PLD_PIN] if isinstance(values, dict) else values[0]

      # Read battery information
      voltage = battery_monitor.readVoltage()
      battery_status = battery_monitor.get_battery_status(voltage)
      capacity = battery_monitor.readCapacity()
      # uart.write((int(22)).to_bytes(2, byteorder='big'))

      # Display current status
      print(f"Battery: {capacity:.1f}% ({battery_status}), Voltage: {voltage:.2f}V, AC Power: {'Plugged in' if ac_power_state == gpiod.line.Value.ACTIVE else 'Unplugged'}")

      # Wait for next monitoring interval
      time.sleep(MONITOR_INTERVAL)