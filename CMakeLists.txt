cmake_minimum_required(VERSION 4.2)
project(BLE_Peripheral)

set(CMAKE_CXX_STANDARD 20)
set(PYBIND11_FINDPYTHON ON)
add_subdirectory(pybind11)

add_executable(BLE_Peripheral main.cpp)
target_include_directories(BLE_Peripheral PRIVATE WiringPi/wiringPi/)
target_link_libraries(BLE_Peripheral PRIVATE pybind11::embed PRIVATE wiringPi)
