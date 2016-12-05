FROM resin/rpi-raspbian:jessie
RUN apt-get update && apt-get install -y \
    python \
    python-numpy \
    python-pip \
    libjpeg-dev \
    python-imaging

RUN pip install paho-mqtt
RUN pip install Pillow --global-option="build_ext" --global-option="--disable-zlib"
ADD receiveImage.py /
CMD ["python","./receiveImage.py"]