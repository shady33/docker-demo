import paho.mqtt.client as mqtt
import base64
import math
import json
import threading
import picamera
import time

packet_size=500

camera = picamera.PiCamera()

def convertImageToBase64():
    with open("output.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
    return encoded

def publishEncodedImage():
    print "Sending New Image"
    encoded = convertImageToBase64()
    end = packet_size
    start = 0
    length = len(encoded)
    picId = "shady"
    pos = 0
    no_of_packets = math.ceil(length/packet_size)
    time_send = int(time.time())
    print "Packet size:" + str(packet_size)
    while start <= len(encoded):
        data = {"data": encoded[start:end], "pos": pos, "size": no_of_packets, "time":time_send}
        client.publish("aalto/image",json.JSONEncoder().encode(data))
        end += packet_size
        start += packet_size
        pos = pos +1
    packet_size += 500

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
#    global camera
#    camera = picamera.PiCamera()
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    sendNewImage()

def sendNewImage():
    global camera
    camera.capture('output.jpg')

    threading.Timer(10.0, sendNewImage).start()
    publishEncodedImage()

client = mqtt.Client()
client.on_connect = on_connect

client.connect("iot.eclipse.org", 1883, 60)

#sendNewImage()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()