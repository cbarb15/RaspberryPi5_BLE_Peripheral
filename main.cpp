#include <iostream>
#include <pybind11/embed.h>
#include <wiringPi.h>
#include <thread>
#include <chrono>

namespace py = pybind11;
using namespace std;

void button_interrupt();

int main() {
    py::scoped_interpreter guard{};
    wiringPiSetup();
    pinMode(4, INPUT);
    pullUpDnControl(4, PUD_DOWN);
    wiringPiISR(4, INT_EDGE_RISING, &button_interrupt);

    while (1) {}
}

void button_interrupt() {
    cout << "Button pushed" << endl;
    // py::module_ peripheral = py::module_::import("peripheral");
    // peripheral.attr("start_advertising_and_create_GATT_app")();
}