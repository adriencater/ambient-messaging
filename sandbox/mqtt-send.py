"""
AM Script for sending message over MQTT:

  - Connect to MQTT Broker for sending a message

"""

import paho.mqtt.client as mqtt
import time
import os
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f'MQTT Connected with result code {reason_code}, {flags}, {userdata}')

def on_publish(client, userdata, mid):
    print('MQTT Data published: ', client, userdata, mid)
 
def on_log(client, userdata, paho_log_level, messages):
    print(messages)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, 'test-client')
mqttc.username_pw_set(os.getenv('AM_MQTT_USER'), os.getenv('AM_MQTT_PASS'))
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_log = on_log
mqttc.connect(os.getenv('AM_MQTT_HOST'), os.getenv('AM_MQTT_PORT') or 1883)
time.sleep(1)

topic = f'ambientmessaging/{sys.argv[1]}'.lower()
message = sys.argv[2]
print(f'Publishing message to topic: {topic}:', message)
mqttc.publish(topic, message)
mqttc.disconnect()
