
import os
import struct
import smbus2
import time
import gpiod
from gpiod.line import Direction
from subprocess import call
import traceback
import multiprocessing

class BatteryMonitor:

   def __init__(self, request):
      self.request = request
      # try:
         # Initialize I2C bus
      self.bus = smbus2.SMBus(1)
      self.address = 0x36

   def readVoltage(self):
      try:
         read = self.bus.read_word_data(self.address, 2)
         swapped = struct.unpack("<H", struct.pack(">H", read))[0]
         voltage = swapped * 1.25 / 1000 / 16
         return voltage
      except Exception:
         return 0

   def readCapacity(self):
      try:
         read = self.bus.read_word_data(self.address, 4)
         swapped = struct.unpack("<H", struct.pack(">H", read))[0]
         capacity = swapped / 256
         return capacity
      except Exception:
         return 0

   def get_battery_status(self, voltage):
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
