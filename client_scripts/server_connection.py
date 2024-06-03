import paho.mqtt.client as mqtt
import sys
from functools import partial
import yaml

config = {}

def on_connect(client: mqtt.Client, userdata, flags, rc, *args, **kwargs):
    if rc == 0:
        print("Connected with result code " + str(rc))
        
        # ------------------------------- REGISTRATION ------------------------------- #
        
        client.subscribe(config['common']['client_prefix'] + kwargs["id"])
        client.publish(config['common']['main_topic'], kwargs["id"])

    else:
        print("Failed to connect, code " + str(rc))
        exit(1)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    if msg.payload.decode() == "QUIT":
        end(client)


def init(id: str) -> mqtt.Client:
    
    with open("config.yaml", 'r') as stream:
        yaml_config = yaml.safe_load(stream)
        
        try:
            global config
            config.update(yaml_config)
        except KeyError as e:
            print("Failed loading configuration", file=sys.stderr)
            raise e
    
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=id)
    client.on_connect = partial(on_connect, id=id)
    client.on_message = on_message

    client.connect(config['client']['broker_address'], config['client']['broker_port'])
    client.loop_start()
    return client


def data_publish(client: mqtt.Client, id:str, message: str):
    client.publish(config['common']['client_prefix'] + id, config['common']['message_types']['data'] + message)

def config_publish(client: mqtt.Client, id:str, message: str):
    client.publish(config['common']['client_prefix'] + id, config['common']['message_types']['config'] + message)

def end(client: mqtt.Client):
    client.loop_stop()
