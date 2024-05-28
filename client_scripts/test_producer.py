import paho.mqtt.client as mqtt
import time
import asyncio

# Define connection parameters
# broker_address = "192.168.0.66"
broker_address = "localhost"
port = 1883
topic = "test"
client_id = "python-mqtt-client-test"

# Define callback functions
def on_connect(client, userdata, flags, rc, *args):
  if rc == 0:
    print("Connected to MQTT Broker!")
  else:
    print("Failed to connect, return code: %d %d",12, rc)

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
client.on_connect = on_connect

client.connect(broker_address, port)

# Start the network loop (in a separate thread)
client.loop_start()

# You can now publish or subscribe to messages here

# Example: Publish a message to the topic
message = "Hello from Python MQTT client!"
client.publish(topic, message)

# Wait for a few seconds for messages to be processed
time.sleep(4)

# Stop the network loop and disconnect
client.loop_stop()
client.disconnect()

print("Disconnected from MQTT Broker")