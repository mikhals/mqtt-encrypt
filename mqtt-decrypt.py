from paho.mqtt import client as mqtt_client

from cryptography.fernet import Fernet
from paho.mqtt import client as mqtt_client

import os


broker = 'public.mqtthq.com'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-2'
# username = 'emqx'
# password = 'public'

if(not os.path.isfile('./key')):
    key = Fernet.generate_key()
    with open('key', 'w') as f:
        f.write(key.decode('utf-8'))

def get_key():
    with open('key') as f:
        content = f.readlines()
    for line in content:
        return line

myKey = get_key()
f = Fernet(myKey)



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        tmp = msg.payload.decode()[2:-1]
        encoded = tmp.encode('utf-8')
        if(msg.payload.decode()[:2] == "b'"):
            print(f.decrypt(encoded))
        else:
            print(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()
