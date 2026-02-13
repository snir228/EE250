import paho.mqtt.client as mqtt
import time

YOUR_USERNAME = "snir"
PING = f"{YOUR_USERNAME}/ping"
PONG = f"{YOUR_USERNAME}/pong"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(PING)
    client.message_callback_add(PING, on_message_from_ping)

def on_message_from_ping(client, userdata, message):
    num = int(message.payload.decode())
    num = num+1
    time.sleep(1)
    client.publish(PONG, str(num))
    print(f"Recieved ping {num-1}, published pong {num}")

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
    client.loop_forever()
