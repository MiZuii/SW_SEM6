import paho.mqtt.client as mqtt

broker_address = "localhost"
port = 1883
topic = "test/topic"
producer_id = "python-mqtt-client-test"
receiver_id = "python-mqtt-receiver-test"

def on_connect(client, userdata, flags, rc, *args):
  if rc == 0:
    print("Connected with result code " + str(rc))
    client.subscribe(topic)
  else:
    print("Failed to connect, code " + str(rc))

def on_message(client, userdata, msg):
  print("Topic: " + msg.topic + "\nMessage: " + msg.payload.decode())

# Create an MQTT client instance
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=receiver_id)

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port)

# Start the network loop to process incoming data
client.loop_forever()