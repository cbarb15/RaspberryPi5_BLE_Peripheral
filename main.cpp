#include <iostream>
#include <pybind11/embed.h>

namespace py = pybind11;
using namespace std;

int main() {
    py::scoped_interpreter guard{};

    py::module_ peripheral = py::module_::import("peripheral");
    peripheral.attr("start_advertising_and_create_GATT_app")();

    return 0;
}
