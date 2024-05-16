"""
AM Service (HTTP Server)

  - Serve static HTML/JS for UI
  - Serve REST API for sending messages over MQTT

"""

import flask
import paho.mqtt.client as mqtt
import time
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

def on_connect(client, userdata, flags, reason_code):
    print(f'MQTT Connected with result code {reason_code}, {flags}, {userdata}')
def on_publish(client, userdata, mid):
    print('MQTT Data published: ', client, userdata, mid)
# mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, 'am-service')
mqttc = mqtt.Client('am-service')
mqttc.username_pw_set(os.getenv('AM_MQTT_USER'), os.getenv('AM_MQTT_PASS'))
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/say/<who>/<message>')
def send(who, message):
    mqttc.connect(os.getenv('AM_MQTT_HOST'), os.getenv('AM_MQTT_PORT') or 1883)
    time.sleep(1)
    topic = f'ambientmessaging/{who}'.lower()
    print(f'MQTT Publishing message to topic: {topic}:', message)
    mqttc.publish(topic, message)
    mqttc.disconnect()
    return flask.jsonify({"topic": topic, "message": message})

# Run server
app.run(host='0.0.0.0', port=9999)
