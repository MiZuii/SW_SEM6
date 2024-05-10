# MQTT GO SRV

### paho mqtt cpp lib installation (for intellisense)

```bash
git clone --branch v1.3.1 \
--recurse-submodules https://github.com/eclipse/paho.mqtt.cpp.git

cd paho.mqtt.cpp

cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_WITH_SSL=OFF

sudo cmake --build build/ --target install

sudo ldconfig
```