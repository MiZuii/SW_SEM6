FROM ubuntu:jammy AS builder

RUN apt-get update && apt-get install -y git cmake build-essential libeigen3-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*

# Build KataGo engine
WORKDIR /app
RUN git clone --branch v1.14.1 https://github.com/lightvector/KataGo.git
WORKDIR /app/KataGo/cpp
RUN cmake . -DUSE_BACKEND=EIGEN -DUSE_AVX2=1
RUN make -j 4

# Clone and build Paho MQTT C++ library
WORKDIR /app
RUN git clone --branch v1.3.1 --recurse-submodules https://github.com/eclipse/paho.mqtt.cpp.git
WORKDIR /app/paho.mqtt.cpp
RUN cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_WITH_SSL=OFF
RUN cmake --build build/ --target install

# MY STAGE
FROM ubuntu:jammy
WORKDIR /app
COPY --from=builder /app/KataGo/cpp/katago /app/katago/katago
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/lib /usr/local/lib

RUN apt-get update && apt-get install -y cmake gcc g++ && rm -rf /var/lib/apt/lists/*
COPY . .
RUN cmake -Bbuild
RUN cmake --build build/

CMD ["./build/main"]