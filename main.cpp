#include <iostream>
#include <pybind11/embed.h>
#include <wiringPi.h>

namespace py = pybind11;
using namespace std;

void button_interrupt();

int main() {
    py::scoped_interpreter guard{};
    // wiringPiSetupGpio();
    wiringPiSetup();
    // pinMode(23, INPUT);
    // pullUpDnControl(23, PUD_DOWN);
    wiringPiISR(13, INT_EDGE_RISING, &button_interrupt);

    // py::module_ peripheral = py::module_::import("peripheral");
    //peripheral.attr("start_advertising_and_create_GATT_app")();

    while (1) {}

    return 0;
}

void button_interrupt() {
    cout << "Button pushed" << endl;
}