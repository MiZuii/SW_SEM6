import paho.mqtt.client as mqtt
from functools import partial

# broker_address = "192.168.0.66"
broker_address = "localhost"
port = 1883
registration_topic = "srv_register"
client_topic_prefix = "client_"


def on_connect(client: mqtt.Client, userdata, flags, rc, *args, **kwargs):
    if rc == 0:
        print("Connected with result code " + str(rc))
        
        # ------------------------------- REGISTRATION ------------------------------- #
        
        client.subscribe(client_topic_prefix + kwargs["id"])
        client.publish(registration_topic, kwargs["id"])

    else:
        print("Failed to connect, code " + str(rc))
        exit(1)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    if msg.payload.decode() == "QUIT":
        end(client)


def init(id: str) -> mqtt.Client:
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=id)
    client.on_connect = partial(on_connect, id=id)
    client.on_message = on_message

    client.connect(broker_address, port)
    client.loop_start()
    return client


def publish(client: mqtt.Client, id:str, message: str):
    client.publish(client_topic_prefix + id, message)

def end(client: mqtt.Client):
    client.loop_stop()
