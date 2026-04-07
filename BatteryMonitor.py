
import os
import struct
import smbus2
import time
import gpiod
from gpiod.line import Direction
from subprocess import call
import traceback
import multiprocessing

SHUTDOWN_THRESHOLD = 3  # Number of consecutive failures required for shutdown
SLEEP_TIME = 60  # Time in seconds to wait between failure checks
MONITOR_INTERVAL = 3  # Seconds between monitoring checks

class BatteryMonitor:

    def __init__(self):
      pid = str(os.getpid())
      pidfile = "/tmp/X1200.pid"
      if os.path.isfile(pidfile):
         exit(1)
      else:
         with open(pidfile, 'w') as f:
            f.write(pid)

      try:
         # Initialize I2C bus
         bus = smbus2.SMBus(1)
         address = 0x36
         
         # Initialize GPIO
         PLD_PIN = 6
         request = gpiod.request_lines(
            '/dev/gpiochip0',
            consumer="PLD",
            config={
                  PLD_PIN: gpiod.LineSettings(direction=Direction.INPUT),
            }
         )

         print(f"Created request {request}")
         failure_counter = 0


      except KeyboardInterrupt:
         pass

      except Exception as e:
         print(f"exception {e}")
         traceback.print_exc()
         pass

      finally:
         # Cleanup
         try:
            if 'request' in locals():
                  request.release()
         except:
            pass
         
         try:
            if 'bus' in locals():
                  bus.close()
         except:
            pass
         
         if os.path.isfile(pidfile):
            os.unlink(pidfile)


      def readVoltage(bus):
         try:
            read = bus.read_word_data(address, 2)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            voltage = swapped * 1.25 / 1000 / 16
            return voltage
         except Exception:
            return 0

      def readCapacity(bus):
         try:
            read = bus.read_word_data(address, 4)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            capacity = swapped / 256
            return capacity
         except Exception:
            return 0

      def get_battery_status(voltage):
         if 3.87 <= voltage <= 4.23:
            return "Full"
         elif 3.7 <= voltage < 3.87:
            return "High"
         elif 3.55 <= voltage < 3.7:
            return "Medium"
         elif 3.4 <= voltage < 3.55:
            return "Low"
         elif voltage < 3.4:
            return "Critical"
         else:
            return "Unknown"
