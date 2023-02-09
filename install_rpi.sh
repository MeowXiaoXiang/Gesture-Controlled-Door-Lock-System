#!/bin/bash

# Check Raspberry Pi OS Version
version=$(lsb_release -a | grep "Release" | awk '{print $2}')
if [ "$version" != "10 (buster)" ]; then
    echo "Error: Mediapipe 只能在 Raspberry Pi OS 10 (buster) 下執行，你的樹梅派版本是 $version."
    exit 1
fi

# Upgrade Numpy
pip3 install -U numpy

# Install OpenCV & dependencies
sudo apt-get install libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test
sudo apt-get install -y libopencv-dev python3-opencv

# Install Mediapipe
pip3 install mediapipe-rpi4

# Install OLED Package
pip3 install luma.oled
