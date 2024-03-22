"""
AM Client

  - Connect to MQTT Broker for receiving messages
  - Display received messages on display (Inkyphat)

"""

from . import core
import paho.mqtt.client as mqtt
import os

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}, {flags}, {userdata}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe('$SYS/#')
    topic = f'ambientmessaging/{client._client_id.decode()}'.lower()
    print('Subscribing to topic:', topic)
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f'Displaying message from topic {msg.topic}: {message}')
    core.display_text(message)

try:
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, os.getenv('AM_CLIENT_NAME') or 'test')
except IndexError:
    raise ValueError('Please set the ID of the client as 1st argument.')
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(os.getenv('AM_MQTT_USER'), os.getenv('AM_MQTT_PASS'))
mqttc.connect(os.getenv('AM_MQTT_HOST'), os.getenv('AM_MQTT_PORT') or 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()
