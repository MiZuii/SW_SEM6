import sys
import paho.mqtt.client as mqtt
from functools import partial
import yaml

config = {}


def on_connect(cid, client, userdata, flags, rc, *args):
    if rc == 0:
        print(f"[{config['common']['session_prefix']+cid}] Connected with result code " + str(rc), file=sys.stderr)
        client.subscribe(config['common']['client_prefix'] + cid)
    else:
        print(f"[{config['common']['session_prefix']+cid}] Failed to connect, code " + str(rc), file=sys.stderr)

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + "\nMessage: " + msg.payload.decode(), file=sys.stderr)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Invalid arguments", file=sys.stderr)
        print("Arg1: ID", file=sys.stderr)
        exit(1)
        
    with open("config.yaml", 'r') as stream:
        yaml_config = yaml.safe_load(stream)
        
        try:
            config.update(yaml_config)
        except KeyError as e:
            print("Failed loading configuration", file=sys.stderr)
            raise e

    cid = sys.argv[1]

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=config['common']['session_prefix'] + cid,
    )

    client.on_connect = partial(on_connect, cid)
    client.on_message = on_message

    client.connect(config['session']['broker_address'], config['session']['broker_port'])

    client.loop_forever()
