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

def async_watch_line_value(chip_path, line_offset, done_fd):
    global uart
    # Assume a button connecting the pin to ground,
    # so pull it up and provide some debounce.
    with gpiod.request_lines(
        chip_path,
        consumer="async-watch-line-value",
        config={
            line_offset: gpiod.LineSettings(
                edge_detection=Edge.BOTH,
                bias=Bias.PULL_UP,
                debounce_period=timedelta(milliseconds=10),
            )
        },
    ) as request:
        poll = select.poll()
        poll.register(request.fd, select.POLLIN)
        # Other fds could be registered with the poll and be handled
        # separately using the return value (fd, event) from poll():
        poll.register(done_fd, select.POLLIN)
        while True:
            for fd, _event in poll.poll():
                if fd == done_fd:
                    # perform any cleanup before exiting...
                    return
                # handle any edge events
                edge_event = request.read_edge_events()[0]
                if edge_event.event_type is edge_event.Type.RISING_EDGE:
                  print("Read Uart")
                  start_advertising_and_create_GATT_app()
            
               
def uart_intterupt_task():
   print("Starting interupt task")
   done_fd = os.eventfd(0)
   try:
      async_watch_line_value("/dev/gpiochip0", 23, done_fd)
   except OSError as ex:
      print(ex, "\nCustomise the example configuration to suit your situation")
      print("background thread exiting...")


def battery_monitor_task():
   battery_monitor = BatteryMonitor()

   failure_counter = 0

   while True:
      # Read GPIO value
      values = battery_monitor.request.get_values()

      ac_power_state = values[battery_monitor.PLD_PIN] if isinstance(values, dict) else values[0]
        
      # Read battery information
      voltage = battery_monitor.readVoltage()
      battery_status = battery_monitor.get_battery_status(voltage)
      capacity = battery_monitor.readCapacity()
        
      # Display current status
      print(f"Battery: {capacity:.1f}% ({battery_status}), Voltage: {voltage:.2f}V, AC Power: {'Plugged in' if ac_power_state == gpiod.line.Value.ACTIVE else 'Unplugged'}")
        
      # Check conditions
      current_failures = 0
        
      if ac_power_state != gpiod.line.Value.ACTIVE:
         current_failures += 1
        
      if capacity < 20:
         current_failures += 1
        
      if voltage < 3.20:
         current_failures += 1
        
      # Update failure counter
      if current_failures > 0:
         failure_counter += 1
      else:
         failure_counter = 0
        
      # Check if shutdown threshold reached
      if failure_counter >= SHUTDOWN_THRESHOLD:
         shutdown_reason = []
         if capacity < 20:
               shutdown_reason.append("critical battery level")
         if voltage < 3.20:
               shutdown_reason.append("critical battery voltage")
         if ac_power_state != gpiod.line.Value.ACTIVE:
               shutdown_reason.append("AC power loss")
            
         reason_text = " and ".join(shutdown_reason)
         print(f"Critical condition met due to {reason_text}. Initiating shutdown.")
            
         # Uncomment to enable actual shutdown
         # call("sudo nohup shutdown -h now", shell=True)
         # break
        
      # Wait for next monitoring interval
      time.sleep(MONITOR_INTERVAL)

if __name__ == '__main__':   
   dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
   bus = dbus.SystemBus()
   
   bat_monitor_task = multiprocessing.Process(target=battery_monitor_task)
   bat_monitor_task.start()
   
   # global uart
   # try: 
   #    uart = serial.Serial("/dev/ttyAMA0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize= serial.EIGHTBITS, timeout=1)
   #    uart_task = multiprocessing.Process(target=uart_intterupt_task)
   #    uart_task.start()
   # except serial.SerialException as e:
   #    serial.close()
   #    print(f"Error opening serial port: {e}")

   while 1:
      pass