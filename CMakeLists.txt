cmake_minimum_required(VERSION 3.16.0)
project(MQTT_GO_SRV)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -pthread -Wall -Wextra -pedantic")

# MAIN TARGET
add_executable(main main.cpp)