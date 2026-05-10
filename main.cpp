#include <iostream>
#include <pybind11/embed.h>
#include <wiringPi.h>
#include <thread>
#include <chrono>

#include "WiringPi/wiringPi/wiringPi.h"

namespace py = pybind11;
using namespace std;

#define IRQpin     16

void button_interrupt();

int main() {
    py::scoped_interpreter guard{};


    wiringPiSetupGpio();

    pinMode(IRQpin, INPUT);
    pullUpDnControl(IRQpin, PUD_UP);

    wiringPiISR(IRQpin, INT_EDGE_FALLING, &button_interrupt);

    while (1) {}
}

void button_interrupt() {
    cout << "Button Pushed" << endl;
}