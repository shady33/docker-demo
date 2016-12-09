# Demo for Docker, Raspberrypi and PiCam

This code shows the basic demo of taking a picture using picamera on the raspberrypi and sending it to a cloud server over mqtt.

It contains two folders:
SendImage
ReceiveImage

SendImage contains the code for encoding an Image into Base64 and sending it over MQTT.
ReceiveImage contains the code for receiving and decoding and Image and calculating its histogram.

To build both dockers go their directories one by one and do:
`docker build -t <name_of_image> .`

To run SendImage do the below command on raspberrypi:

`docker run --device /dev/vchiq -t <name_of_image>`

To run ReceiveImage do the below command on raspberrypi:

`docker run -t <name_of_image>`

