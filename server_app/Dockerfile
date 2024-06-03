FROM alpine AS builder

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    git \
    make \
    cmake \
    musl-dev \
    eigen-dev \
    zlib

# Clone and build Paho MQTT C++ library
WORKDIR /app
RUN git clone --branch v1.3.1 --recurse-submodules https://github.com/eclipse/paho.mqtt.cpp.git
WORKDIR /app/paho.mqtt.cpp
RUN cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_WITH_SSL=OFF
RUN cmake --build build/ --target install

WORKDIR /app
RUN git clone --branch 0.8.0 https://github.com/jbeder/yaml-cpp.git
RUN mkdir /app/yaml-cpp/build
WORKDIR /app/yaml-cpp/build
RUN cmake -DYAML_BUILD_SHARED_LIBS=ON ..
RUN make -j4 install

# MY STAGE
FROM python:3.10-alpine
WORKDIR /app
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/lib /usr/local/lib

RUN apk add make cmake gcc g++
COPY . .
RUN cmake -Bbuild
RUN cmake --build build/

RUN python3 -m pip install paho-mqtt pyyaml python-dotenv requests python-socketio websocket-client

CMD ["/app/build/main", "/usr/local/bin/python3", "/app/session.py"]