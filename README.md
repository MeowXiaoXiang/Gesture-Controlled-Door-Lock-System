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

1. 確認樹莓派系統架構與硬體版本
首先，您需要確認自己的 Raspberry Pi 系統架構以及硬體版本，這將決定後續您需要安裝的 Mediapipe 版本。

> **提示**：如果您不確定應該選擇哪個版本，且您的 Raspberry Pi 是 3 代或 4 代，個人推薦使用 [**Raspberry Pi OS (Legacy)**](https://downloads.raspberrypi.com/raspios_oldstable_armhf/images/raspios_oldstable_armhf-2022-01-28/2022-01-28-raspios-buster-armhf.zip)。這是我個人使用過且沒有問題的版本，穩定支援 32-bit 的 Mediapipe 版本。

- **檢查系統架構**：
  在 **Raspberry Pi** 的終端機輸入以下命令：
  ```bash
  uname -m
  ```
  如果結果顯示：
  - `armv7l`：表示您使用的是 32-bit 系統架構（Raspberry Pi OS 32-bit）。
  - `aarch64`：表示您使用的是 64-bit 系統架構（Raspberry Pi OS 64-bit）。

- **確認硬體版本**：
  如果架構是 `armv7l`，則需要進一步判斷您使用的是 Raspberry Pi 3 還是 Raspberry Pi 4。
  - **Raspberry Pi 3** 的特徵：有一個標準 HDMI 接口（較大）。
  - **Raspberry Pi 4** 的特徵：有兩個小的 Mini HDMI 接口。

  您也可以通過命令查詢具體硬體型號：
  ```bash
  cat /proc/cpuinfo | grep 'Model'
  ```

  根據以上資訊，確認您的設備並記錄下來以進行後續步驟。

2. 更新所有套件
在進行安裝前，建議更新所有系統套件以確保安裝過程順利：

  ```bash
  sudo apt update
  sudo apt upgrade
  ```

3. 安裝 NumPy
首先安裝或升級 NumPy，這是後續 OpenCV 和 Mediapipe 的必要依賴：

  ```bash
  pip3 install numpy
  ```

4. 安裝 OpenCV 及依賴項
接著安裝 OpenCV 及其依賴項：

- 安裝依賴項：
  ```bash
  sudo apt install libatlas-base-dev
  ```

- 安裝 OpenCV：
  ```bash
  pip3 install opencv-python
  ```

5. 安裝 Mediapipe
根據您先前確認的系統架構與硬體版本，選擇安裝適當的 Mediapipe 版本：

- **若系統架構為 `armv7l` (32-bit)**：
  - **Raspberry Pi 3**：
    ```bash
    pip3 install mediapipe-rpi3
    ```
  - **Raspberry Pi 4**：
    ```bash
    pip3 install mediapipe-rpi4
    ```

- **若系統架構為 `aarch64` (64-bit)**：
    ```bash
    pip3 install mediapipe
    ```

> **提示**：Mediapipe 是系統架構依賴的軟體包，請務必依據您的架構安裝正確版本。

6. 安裝 OLED 套件
因為有使用 OLED 顯示器，請安裝相關的套件：
  ```bash
  pip3 install luma.oled
  ```

7. 安裝 Loguru
最後，安裝 Loguru，用於日誌處理：
  ```bash
  pip3 install loguru
  ```

8. 修改 [main.py](main.py) 的 **可調整區域** 來符合你的要求

9. 修改 **Raspberry Pi** 設定，啟動I2C

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
* [手部21个关键点检测+手势识别-[MediaPipe]](https://blog.csdn.net/weixin_45930948/article/details/115444916) by [开鑫9575](https://blog.csdn.net/weixin_45930948)
* [finish_ben](https://github.com/benben-ub/finish_ben) by [benben-ub](https://github.com/benben-ub)
