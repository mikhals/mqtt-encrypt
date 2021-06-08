# python 3.6
import time
import random
import time
from cryptography.fernet import Fernet
from paho.mqtt import client as mqtt_client
import os

if(not os.path.isfile('./key')):
    key = Fernet.generate_key()
    with open('key', 'w') as f:
        f.write(key.decode('utf-8'))

def get_key():
    with open('key') as f:
        content = f.readlines()
    for line in content:
        print(line)
        return line

myKey = get_key()
f = Fernet(myKey)

def encrypt(m):
    return f.encrypt(m.encode('utf-8'))

broker = 'public.mqtthq.com'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

connected = False
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        global connected
        if rc == 0:
            print("Connected to MQTT Broker!")
            connected = True
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,message):
    time.sleep(1)
    msg = f"{message}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    while(not connected):
        time.sleep(1)
    myMessage = "Hello this is encrypted"
    publish(client,encrypt(myMessage))

run()
