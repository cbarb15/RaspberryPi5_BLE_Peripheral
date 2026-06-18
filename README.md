# <ins>Libraries To Include</ins>

* pip3 install adafruit-circuitpython-ads1x15
* sudo apt install git virtualenv build-essential python3-dev libdbus-glib-1-dev libgirepository1.0-dev
* pip3 install dbus-python
* pip3 install pycairo (If pycairo fails, run sudo apt install libcairo2-dev pkg-config python3-dev first. Then re install pycairo)  
* pip3 install PyGObject
* pip3 install adafruit-extended-bus
* pip3 install gpiod

<ins>If error can't find module lgpio when importing digitalio</ins>

Run:

* sudo apt-get install swig python3-lgpio liblgpio-dev python3-setuptools python-dev-is-python3
* pip3 install lgpio


This project now uses pybind to call the Peripheral functions. It is using Pybind and will need to be cloned. Will also be using WiringPi.
