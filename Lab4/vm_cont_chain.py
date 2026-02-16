"""EE 250L Lab 04 Continue Chain"""

# Steve Cho (USC ID: 4314516349)
# Sivan Nir (USC ID: 7594069996)

import paho.mqtt.client as mqtt
import time

# Call back function that gets celled when the client and the MQTT broker on RPi is successfully connected
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("smcho/ping")
    client.message_callback_add("smcho/ping", on_message_from_ping)


"""This object (functions are objects!) serves as the default callback for 
messages received when another node publishes a message this client is 
subscribed to. By "default,"" we mean that this callback is called if a custom 
callback has not been registered using paho-mqtt's message_callback_add()."""
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

# Ping message callback.
def on_message_from_ping(client, userdata, message):
    num = int(message.payload.decode("utf-8"))
    num = num+1
    time.sleep(1)
    client.publish("smcho/pong", str(num))
    print(f"Received Ping {num-1}, Published Pong {num}")


if __name__ == '__main__':
    
    # Create a client object
    client = mqtt.Client()
    # Attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    # Attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    # Connect to the RPi Broker
    client.connect(host="172.20.10.3", port=1883, keepalive=60)
    # Ensures the client loops forever
    client.loop_forever()