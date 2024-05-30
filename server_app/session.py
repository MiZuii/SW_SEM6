import sys
import paho.mqtt.client as mqtt
from functools import partial

# broker_address = "192.168.0.66"
broker_address = "broker"
port = 1883
session_prefix = "session_"
client_prefix = "client_"


def on_connect(cid, client, userdata, flags, rc, *args):
    if rc == 0:
        print(f"[{session_prefix+cid}] Connected with result code " + str(rc), file=sys.stderr)
        client.subscribe(client_prefix + cid)
    else:
        print(f"[{session_prefix+cid}] Failed to connect, code " + str(rc), file=sys.stderr)


def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + "\nMessage: " + msg.payload.decode(), file=sys.stderr)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Invalid arguments", file=sys.stderr)
        print("Arg1: ID", file=sys.stderr)
        exit(1)

    cid = sys.argv[1]

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=session_prefix + cid,
    )

    client.on_connect = partial(on_connect, cid)
    client.on_message = on_message

    client.connect(broker_address, port)

    client.loop_forever()
