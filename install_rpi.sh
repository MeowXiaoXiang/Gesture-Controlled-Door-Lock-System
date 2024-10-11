#!/bin/bash
# Bash script

echo "這可能要花費些時間，請耐心等待。"

# Detect Raspberry Pi OS Architecture
architecture=$(uname -m)
version=$(lsb_release -r | awk '{print $2}')
codename=$(lsb_release -c | awk '{print $2}')
pi_model=$(cat /proc/cpuinfo | grep "Model" | awk '{$1=$2=""; sub(/^ +/, ""); print $0}')
# 顯示給使用者看詳細資訊
echo "[$pi_model]"
echo "Raspberry Pi OS 資訊"
echo "作業系統架構: $architecture"
echo "作業系統版本: $version 代號: $codename"

read -p "是否要先更新所有套件? (按 Enter 開始更新，或輸入 'n' 跳過): " run_update

if [ "$run_update" != "n" ]; then
    echo "正在執行 'sudo apt update && sudo apt -y upgrade'..."
    sudo apt update && sudo apt -y upgrade
    echo "更新完成"
else
    echo "跳過更新"
fi

# 先安裝和升級必要的依賴項
# 升級 Numpy
echo "正在升級 Numpy..."
pip3 install numpy

# 安裝 OpenCV 及其依賴項
echo "正在安裝 OpenCV 及其依賴項..."
sudo apt install -y libatlas-base-dev
pip3 install opencv-python

# 根據架構選擇安裝 Mediapipe 的方式
if [ "$architecture" = "armv7l" ]; then
    echo "已確認架構為 $architecture，開始安裝 Mediapipe..."

    # 判斷是樹莓派3還是4
    if [ "$(echo $pi_model | awk '{print $3}')" = "3" ];then
        pip3 install mediapipe-rpi3
    else
        pip3 install mediapipe-rpi4
    fi

elif [ "$architecture" = "aarch64" ]; then
    echo "已確認架構為 $architecture，開始安裝 Mediapipe..."
    pip3 install mediapipe
else
    echo "警告: 未知架構 ($architecture)，將嘗試安裝 Mediapipe..."
    pip3 install mediapipe
fi

# 最後安裝 loguru 和 luma.oled
echo "正在安裝 loguru..."
pip3 install loguru

echo "正在安裝 OLED Package..."
pip3 install luma.oled

echo "安裝完成！"
