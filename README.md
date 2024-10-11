# [專題] 手勢控制門鎖系統

* 這個專題使用MediaPipe和OpenCV進行手勢辨識，並有簡易的密碼設定網頁。
* 當有設定密碼時，會透過Webcam辨識手勢輸入密碼，預設支援0~9與比出大拇指讚的手勢。輸入正確密碼後比讚將進行開門動作。
* 若密碼錯誤次數超過3次，則會清除密碼，需要重新設定才可使用。
* 目前在這個項目有提供關於伺服馬達的程式，不過僅限參考，若不同的話，親手改看看吧。

## Installation

* 若要快速安裝可使用 [install_rpi.sh](install_rpi.sh)
  請在此專案目錄下在 **Raspberry Pi** 的終端機輸入以下命令
  ```bash
  sudo chmod a+x install_rpi.sh
  ./install_rpi.sh
  ```

1. 確認 **Raspberry Pi** 作業系統的 Debian 版本為 `10 (buster)` 或 `11 (bullseye)` 且架構為 `aarch64`
   * **Raspberry Pi** 的終端機並輸入 `lsb_release -a` 檢查版本，輸入 `uname -m` 檢查架構
   * 若版本為 `11 (bullseye)` 架構為 `armv7l` 請下載 [Raspberry Pi Imager](https://www.raspberrypi.com/software/) 並選擇安裝 `Raspberry Pi OS (Legacy)` 或 `Raspberry Pi OS (64-bit)`
2. 更新所有套件
   ```bash
   sudo apt update
   sudo apt upgrade
   ```
4. 安裝OpenCV & 依賴項:
   * 安裝依賴項
     ```bash
     sudo apt install libatlas-base-dev
     ```
   * 安裝 OpenCV
     ```bash
     pip3 install opencv-python==4.6.0.*
     ```
5. 安裝特定版本的 NumPy
   ```bash
   pip3 install numpy==1.21.6
   ```
6. 安裝Mediapipe
    * 若樹梅派使用了32-bit的架構的 Raspberry Pi OS
      * Raspberry Pi 3 :
        ```bash
        pip3 install mediapipe-rpi3
        ```
      * Raspberry Pi 4 :
        ```bash
        pip3 install mediapipe-rpi4
        ```
    * 若樹梅派是使用 Raspberry Pi OS (64-bit)
        ```bash
        pip3 install mediapipe
        ```
7. 降低`protobuf`套件版本至`3.20.*`
   ```bash
   pip3 install protobuf==3.20.*
   ```
8. 安裝 OLED 套件
   ```bash
   pip3 install luma.oled
   ```
10. 修改 [main.py](main.py) 的 **可調整區域** 來符合你的要求

11. 修改 **Raspberry Pi** 設定，啟動I2C

![I2C 設定](https://raw.githubusercontent.com/MeowXiaoXiang/Gesture-Controlled-Door-Lock-System/master/markdown_img/raspi_config.png)

* 如要在 Windows 上測試，直接用以下指令安裝套件即可，並設定 [main.py](main.py) 的 **可調整區域** 來符合你的要求
  * `pip install -r requirements_win.txt`

## User Guide

1. 首先進入 [http://127.0.0.1:8080/](http://127.0.0.1:8080/) (會受到你設定的Port影響)
2. 在網頁上設定密碼和密碼時效，並點擊 **「送出設定」** 按鈕。
3. 輸入密碼的方式是在 **WebCam** 前面用單手比出數字，**OLED** 會顯示您已輸入的密碼。
4. 確認密碼無誤後再比出**讚**的手勢，門就會開開。若錯誤三次，則會清除密碼。

## Wiring diagram
![接線圖](https://raw.githubusercontent.com/MeowXiaoXiang/Gesture-Controlled-Door-Lock-System/master/markdown_img/wiring_diagram.jpg)

---
## 參考資料
- [手部21个关键点检测+手势识别-[MediaPipe]](https://blog.csdn.net/weixin_45930948/article/details/115444916) by [开鑫9575](https://blog.csdn.net/weixin_45930948)
<br>
- [finish_ben](https://github.com/benben-ub/finish_ben) by [benben-ub](https://github.com/benben-ub)
