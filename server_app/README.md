# MQTT GO SRV

## Server setup
To run the server use the `docker_compose.yaml` in main project directory. There is also optional file that doesnt run local broker.
Cmd to run the compose:
```bash
docker compose -f docker_compose.yaml up
# for detached terminal
docker compose -f docker_compose.yaml up -d
```
Cmd to delete the compose:
```bash
docker compose -f docker_compose.yaml down
```

### paho mqtt cpp lib installation (for intellisense)

```bash
git clone --branch v1.3.1 \
--recurse-submodules https://github.com/eclipse/paho.mqtt.cpp.git

cd paho.mqtt.cpp

cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_WITH_SSL=OFF

sudo cmake --build build/ --target install

sudo ldconfig
```