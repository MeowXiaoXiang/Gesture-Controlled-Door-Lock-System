# [專題] 手勢控制門鎖系統

* 這個專題使用MediaPipe和OpenCV進行手勢辨識，並有簡易的密碼設定網頁。
* 當有設定密碼時，會透過Webcam辨識手勢輸入密碼，預設支援0~9與比出大拇指讚的手勢。輸入正確密碼後比讚將進行開門動作。
* 若密碼錯誤次數超過3次，則會清除密碼，需要重新設定才可使用。
* 目前在這個項目沒有提供關於伺服馬達的程式，親手寫看看吧。

## Installation

* 若要快速安裝可使用 [install_rpi.sh](install_rpi.sh)
  請在此專案目錄下在 **Raspberry Pi** 的終端機輸入以下命令
  * `bash install_rpi.sh`

1. 確認 **Raspberry Pi** 作業系統的 Debian 版本為 `10 (buster)`
   * **Raspberry Pi** 的終端機並輸入 `lsb_release -a` 檢查版本
   * 若版本為 `11 (bullseye)` 請下載 [Raspberry Pi Imager](https://www.raspberrypi.com/software/) 並選擇安裝 `Raspberry Pi OS (Legacy)`
2. 升級 NumPy
   * `pip3 install -U numpy`
3. 安裝OpenCV & 依賴項:
   * 安裝依賴項
     * `sudo apt-get install libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test`
   * 安裝 OpenCV
     * `sudo apt-get install -y libopencv-dev python3-opencv`
4. 安裝Mediapipe
   * `pip3 install mediapipe-rpi4`
5. 安裝 OLED 套件
   * `pip3 install luma.oled`
6. 修改 [main.py](main.py) 的 **可調整區域** 來符合你的要求

7. 修改 **Raspberry Pi** 設定，啟動I2C

![I2C 設定](https://raw.githubusercontent.com/MeowXiaoXiang/Gesture-Controlled-Door-Lock-System/master/markdown_img/raspi_config.png)

* 如要在 Windows 上測試，直接用以下指令安裝套件即可，並設定 [main.py](main.py) 的 **可調整區域** 來符合你的要求
  * `pip install -r requirements_win.txt`

## User Guide

1. 首先進入 [http://127.0.0.1:8080/](http://127.0.0.1:8080/) 這個網頁。(可能受到你設定的Port影響)
2. 在網頁上設定密碼和密碼時效，並點擊 **「送出設定」** 按鈕。
3. 輸入密碼的方式是在 **WebCam** 前面用單手比出數字，**OLED** 會顯示您已輸入的密碼。
4. 確認密碼無誤後再比出**讚**的手勢，門就會開開。若錯誤三次，則會清除密碼。

## Wiring diagram
![接線圖](https://raw.githubusercontent.com/MeowXiaoXiang/Gesture-Controlled-Door-Lock-System/master/markdown_img/wiring_diagram.jpg)
