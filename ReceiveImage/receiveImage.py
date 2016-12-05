import paho.mqtt.client as mqtt
import json
from PIL import Image
import numpy as np

imageString = []
cnt = 0

def calculateHist():
    img = Image.open('imageToSave.jpg')
    img.load()
    hist, bin_edges = np.histogram(img)
    print "Histogram:" 
    print hist

def reConstructImage(data):
    global imageString,cnt
    data_decode = json.loads(data)
    if imageString == []:
        imageString = [None] * int(data_decode['size']+1)
    
    imageString[data_decode['pos']] = data_decode['data']
    cnt += 1
    if cnt == data_decode['size']+1:
        imgData = ''.join(imageString)
        with open("imageToSave.jpg", "wb") as fh:
            fh.write(imgData.decode('base64'))
        print "New image received"
        calculateHist()
        imageString = []
        cnt = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("aalto/image")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    reConstructImage(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()