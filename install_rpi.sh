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
pip3 install numpy==1.21.6

# Install OpenCV & dependencies
sudo apt-get install libatlas-base-dev
pip3 install opencv-python==4.6.0.*

# Install Mediapipe
pip3 install mediapipe-rpi4

# Install OLED Package
pip3 install luma.oled

echo "安裝完成！"
