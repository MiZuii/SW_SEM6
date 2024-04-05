## local broker setup

Run in `./` directory soo that the `client_scripts/mosquitto.conf` path matches

```bash
docker run \
    -p 1883:1883 \
    --expose 1883 \
    -v ./client_scripts/mosquitto.conf:/mosquitto/config/mosquitto.conf \
    eclipse-mosquitto:latest
```
