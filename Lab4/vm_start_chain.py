import paho.mqtt.client as mqtt
import time

YOUR_USERNAME = "snir"
PING = f"{YOUR_USERNAME}/ping"
PONG = f"{YOUR_USERNAME}/pong"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(PONG)
    client.message_callback_add(PONG, on_message_from_pong)

def on_message_from_pong(client, userdata, message):
    num = int(message.payload.decode())
    num = num+1
    time.sleep(1)
    client.publish(PING, str(num))
    print(f"Recieved pong {num-1}, published ping {num}")

if __name__ == '__main__':
    #get IP address
    ip_address="172.20.10.3"
    """your code here"""
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)

    count=0
    time.sleep(1)
    client.publish(PING, str(count))
    print(f"published ping {count}")

    while True:
        time.sleep(1)
