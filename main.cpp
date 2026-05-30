#include <iostream>
#include <pybind11/embed.h>
#include <wiringPi.h>
#include <wiringSerial.h>
#include <thread>
#include <chrono>

#include "WiringPi/wiringPi/wiringPi.h"
#include "WiringPi/wiringPi/wiringSerial.h"

// #include "WiringPi/wiringPi/wiringPi.h"

namespace py = pybind11;
using namespace std;

#define BLEButtonIrqPin     16
#define AutoModeIrqPin      26

void BLEButtonInterrupt();
void AutoModeEngageButtonInterrupt();

int main() {
    int fd;

    wiringPiSetupGpio();

    pinMode(BLEButtonIrqPin, INPUT);
    pullUpDnControl(BLEButtonIrqPin, PUD_DOWN);
    pinMode(AutoModeIrqPin, INPUT);
    pullUpDnControl(AutoModeIrqPin, PUD_DOWN);

    wiringPiISR(BLEButtonIrqPin, INT_EDGE_RISING, &BLEButtonInterrupt);
    wiringPiISR(AutoModeIrqPin, INT_EDGE_FALLING, &AutoModeEngageButtonInterrupt);
  
    // fd = serialOpen("/dev/ttyAMA0", 115200);
    // if (fd < 0) {
    //     cout << "Unable to open serial device" << endl;
    // }

    while (1) {
        this_thread::sleep_for(std::chrono::seconds(10));
        // digitalWrite(AutoModeIrqPin, HIGH);
        //
        // this_thread::sleep_for(std::chrono::seconds(1));
        // digitalWrite(AutoModeIrqPin, LOW);
        // this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void BLEButtonInterrupt() {
    // py::scoped_interpreter guard{};
    // py::module_ peripheralModule = py::module_::import("peripheral");
    cout << "Start Adv" << endl;
    // peripheralModule.attr("start_advertising_and_create_GATT_app")();
}

void AutoModeEngageButtonInterrupt() {
    cout << "Engage Auto Mode" << endl;
}