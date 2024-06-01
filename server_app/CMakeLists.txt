cmake_minimum_required(VERSION 3.16.0)
project(MQTT_GO_SRV)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -pthread -Wall -Wextra -pedantic")

find_package(PahoMqttCpp REQUIRED)
include_directories(hdr)

# MAIN TARGET
add_executable(main src/main.cpp)
target_link_libraries(main -lyaml-cpp)

# target_link_libraries(data_publish paho-mqtt3a paho-mqttpp3)
target_link_libraries(main PahoMqttCpp::paho-mqttpp3)