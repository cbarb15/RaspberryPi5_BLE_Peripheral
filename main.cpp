#include <iostream>
#include <pybind11/embed.h>
#include <wiringPi.h>
#include <wiringSerial.h>
#include <thread>
#include <chrono>

#include "WiringPi/wiringPi/wiringSerial.h"

// #include "WiringPi/wiringPi/wiringPi.h"

namespace py = pybind11;
using namespace std;

#define IRQpin     16

void button_interrupt();

int main() {
    int fd;

    wiringPiSetupGpio();

    pinMode(IRQpin, INPUT);
    pullUpDnControl(IRQpin, PUD_UP);

    wiringPiISR(IRQpin, INT_EDGE_FALLING, &button_interrupt);
    // fd = serialOpen("/dev/ttyAMA0", 115200);
    // if (fd < 0) {
    //     cout << "Unable to open serial device" << endl;
    // }

    while (1) {
       //  serialPutchar(fd, 'h');
       //
       // this_thread::sleep_for(std::chrono::seconds(3));
    }
}

void button_interrupt() {
    py::scoped_interpreter guard{};
    py::module_ peripheralModule = py::module_::import("peripheral");
    cout << "Start Adv" << endl;
    peripheralModule.attr("start_advertising_and_create_GATT_app")();
}