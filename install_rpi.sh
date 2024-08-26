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

if [ "$architecture" == "armv7l" ]; then
    # 若是 Raspberry Pi OS (Buster) 32-bit (armv7l)
    if [ "$version" == "11" ]; then
        echo "錯誤: Mediapipe 目前確認只能在以下作業系統版本或架構執行:"
        echo "Raspberry Pi OS 10 (Buster) 32-bit (armv7l)"
        echo "Raspberry Pi OS 11 (Bullseye) 64-bit (aarch64)"
        echo "可以去 Raspberry Pi OS 官方網站利用 Raspberry Pi Imager 下載並安裝 Raspberry Pi OS (Legacy) 或 Raspberry OS (64-bit)"
        echo "Raspberry Pi OS 官方網站: https://www.raspberrypi.com/software/"
        exit 1
    elif [ "$version" == "10" ]; then
        echo "已確認版本為 $version ($codename) 繼續進行安裝..."
    fi
elif [ "$architecture" == "aarch64" ]; then
        echo "已確認架構為 $architecture 繼續進行安裝..."
else
    echo "警告: 不支援或無法確定是否支援的架構 ($architecture)"
    read -p "繼續執行安裝指令檔? (按 Enter 繼續安裝，或輸入 'n' 退出): " continue_execution
    if [ "$continue_execution" != "n" ]; then
        echo "繼續進行安裝套件..."
    else
        echo "結束指令檔案"
        exit 1
    fi
fi

# Install loguru
pip3 install loguru

# Install OpenCV & dependencies
sudo apt install -y libatlas-base-dev
pip3 install opencv-python==4.6.0.*

# Upgrade Numpy
pip3 install numpy==1.21.6

# Install Mediapipe
if [ "$architecture" == "armv7l" ]; then
    if [ "$(pi_model | awk '{print $3}')" = "3" ]; then
        pip3 install mediapipe-rpi3
    else
        pip3 install mediapipe-rpi4
    fi
else
    pip3 install mediapipe
fi

# Downgrade protobuf to 3.20.*
pip3 install protobuf==3.20.*

# Install OLED Package
pip3 install luma.oled

echo "安裝完成！"
