#include <iostream>
#include <pybind11/embed.h>

namespace py = pybind11;
using namespace std;

int main() {
    py::scoped_interpreter guard{};

    py::print("Hello World!");

}
