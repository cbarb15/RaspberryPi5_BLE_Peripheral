cmake_minimum_required(VERSION 4.2)
project(BLE_Peripheral)

set(CMAKE_CXX_STANDARD 20)
set(PYBIND11_FINDPYTHON ON)
add_subdirectory(pybind11)

#pybind11_add_module(math_module add.cpp)
#install(TARGETS math_module DESTINATION .)
add_executable(BLE_Peripheral main.cpp)
target_link_libraries(BLE_Peripheral PRIVATE pybind11::embed)