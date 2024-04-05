FROM alpine:3.17 AS builder

RUN apk add --no-cache git cmake build-base
WORKDIR /app

# Clone and build Paho MQTT C++ library
RUN git clone --branch v1.3.1 --recurse-submodules https://github.com/eclipse/paho.mqtt.cpp.git
WORKDIR /app/paho.mqtt.cpp
RUN cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_WITH_SSL=OFF
RUN cmake --build build/ --target install

# MY STAGE
FROM builder
WORKDIR /app
COPY . .
RUN cmake -Bbuild
RUN cmake --build build/

CMD ["./build/main"]