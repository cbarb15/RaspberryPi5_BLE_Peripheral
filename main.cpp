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

#define BLE_BUTTON_IRQ_PIN  16
#define AUTO_MODE_IRQ_PIN   26
#define POWER_OFF_IRQ_PIN   19

void bleButtonInterrupt();
void autoModeEngageButtonInterrupt();
void powerOffButtonInterrupt();

int main() {
    int fd;

    wiringPiSetupGpio();

    pinMode(BLE_BUTTON_IRQ_PIN, INPUT);
    pullUpDnControl(BLE_BUTTON_IRQ_PIN, PUD_DOWN);
    pinMode(AUTO_MODE_IRQ_PIN, INPUT);
    pullUpDnControl(AUTO_MODE_IRQ_PIN, PUD_DOWN);
    pinMode(POWER_OFF_IRQ_PIN, INPUT);
    pullUpDnControl(POWER_OFF_IRQ_PIN, PUD_DOWN);

    wiringPiISR(BLE_BUTTON_IRQ_PIN, INT_EDGE_RISING, &bleButtonInterrupt);
    wiringPiISR(AUTO_MODE_IRQ_PIN, INT_EDGE_RISING, &autoModeEngageButtonInterrupt);
    wiringPiISR(POWER_OFF_IRQ_PIN, INT_EDGE_RISING, &powerOffButtonInterrupt);

    // fd = serialOpen("/dev/ttyAMA0", 115200);
    // if (fd < 0) {
    //     cout << "Unable to open serial device" << endl;
    // }

    while (1) {

   }
}

void bleButtonInterrupt() {
    // py::scoped_interpreter guard{};
    // py::module_ peripheralModule = py::module_::import("peripheral");
    cout << "Start Adv" << endl;
    // peripheralModule.attr("start_advertising_and_create_GATT_app")();
}

void autoModeEngageButtonInterrupt() {
    cout << "Engage Auto Mode" << endl;
}

void powerOffButtonInterrupt() {
    cout << "POWER OFF" << endl;
}