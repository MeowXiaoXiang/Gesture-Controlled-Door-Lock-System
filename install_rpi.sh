#!/bin/bash

echo "這可能要花費些時間，請耐心等待。"
# Check Raspberry Pi OS Version
version=$(lsb_release -a | grep "Release" | awk '{print $2}')
if [ "$version" != "10" ]; then
    echo "Error: Mediapipe 只能在 Raspberry Pi OS 10 (buster) 下執行，你的 Raspberry Pi OS 版本是 $version"
    echo "可以去 Raspberry Pi OS 官方網站下載 Raspberry Pi Imager 選擇安裝 Raspberry Pi OS (Legacy)"
    exit 1
fi

# Install loguru
pip3 install loguru

# Upgrade Numpy
pip3 install -U numpy

# Install OpenCV & dependencies
sudo apt-get install libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test
sudo apt-get install -y libopencv-dev python3-opencv

# Install Mediapipe
pip3 install mediapipe-rpi4

# Install OLED Package
pip3 install luma.oled

echo "安裝完成！"
