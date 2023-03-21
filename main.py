import time
# import RPi.GPIO as GPIO # 若是樹梅派要使用的話請移除註解 "#" 
import threading
from GestureDetection import GestureDetector
from loguru import logger
from flask import Flask, render_template, request
# ---------------------可調整區域----------------------
I2C_OLED = False           # 是否啟用OLED，未開啟會在終端機出現
cv2_Screen = True          # 顯示偵測手指的畫面(省資源可以設定成False關閉)
detection_Interval = 1.5   # 偵測間隔時間(單位:秒)
errorCount = 3             # 密碼錯誤次數
servoMotor = False         # 啟用伺服馬達
# ---------------------------------------------------
Password = None            # 設定的密碼 (網頁設定)
enteredPassword = ""      # 正在輸入的密碼
validityTime = None     # 密碼有效時間 (單位:秒) (用於網頁設定)
start_validityTime = None # 密碼有效時間的開始記錄時間 (用於記錄被設定密碼的開始時間)
# ------GPIO伺服馬達輸出設定區域 (樹梅派)(僅供參考)---------

def operate_motor(freq:int=50): -> None
    """
    控制伺服馬達開關，可調整裡面的degrees來決定動作。
    :param freq: int，伺服馬達頻率控制，預設50。
    """
    if servoMotor:
        motorPin = 18            # 腳位 18
        GPIO.setmode(GPIO.BCM)   # GPIO模式
        GPIO.setup(motorPin, GPIO.OUT) # 輸出腳位OUT
        SG90=GPIO.PWM(motorPin, freq)  # 建立實體物件, 腳位, 頻率
        SG90.start(0)            # 開始

        def duty_cycle_angle(angle=0):
            duty_cycle = (0.05*freq) + (0.19*freq*angle/180)
            return duty_cycle

        def move(degree, wait_time):
            duty_cycle = duty_cycle_angle(degree)
            # print(f"{degree}度 = {duty_cycle}週期")
            SG90.ChangeDutyCycle(duty_cycle)
            time.sleep(wait_time)

        degrees = [50, 150, 50] #50關 150開 50關
        for _ in range(3):
            for degree in degrees:
                move(degree, wait_time=0.35)

        SG90.stop()
        GPIO.cleanup()
# ---------------------------------------------------

# ----------- I2C OLED 點矩陣液晶顯示器(樹梅派)(僅供參考---
if I2C_OLED:
    from luma.core.interface.serial import i2c, spi
    from luma.core.render import canvas
    from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
# ---------------------------------------------------

# ----------------- Flask 架設的網頁------------------
# 對應html如下
# passinput  輸入欄位
# send       送出按鈕
# timeliness 時效性

app = Flask(__name__, static_url_path ='/static/')
@app.route('/',methods=['POST','GET'])
def index():
    global Password, validityTime, start_validityTime
    if request.method =='POST':
        if request.values['send']=='送出':
            Password = request.values['passinput']
            validityTime = float(request.values['timeliness'])
            logger.info("密碼已設定")
            #---------時效性計時----------
            start_validityTime = time.time()
            #----------------------------
            return render_template('index.html', tip=f"密碼已設定完成為:{Password}<br>有效時間為{validityTime}秒")
    return render_template('index.html',tip="請輸入你要設定的密碼")
# -------------------- OLED控制 ----------------------
oled_cache = [] # OLED 的暫存
def oled_control(text_list):
    """
    更新OLED顯示，使用新的字串list。
    :param text_list: list，包含2行要在OLED上顯示的字串。 [第一行, 第二行]
    """
    global oled_cache
    if oled_cache != text_list:
        oled_cache = text_list
        try:
            if I2C_OLED:
                device.cleanup = ""
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    if len(text_list[0]) < 15:
                        draw.text((30, 20), F"{text_list[0]}\n{text_list[1]}", fill="white")
                    else:
                        draw.text((20, 20), F"{text_list[0]}\n{text_list[1]}", fill="white")
            else:
                for index in range(2):
                    logger.debug(F"OLED 正在顯示: {text_list[index]}")
        except Exception as e:
            logger.error(F"OLED顯示發生錯誤: {e}")
# ---------------------------------------------------
detector = GestureDetector()
def main():
    global Password, enteredPassword, start_validityTime, errorCount
    while True:
        if Password:
            if str(detector.dtnum) != "Great":
                enteredPassword += str(detector.dtnum) if detector.dtnum else ""
                oled_control(['Enter Password:', enteredPassword])
            elif str(detector.dtnum) == "Great" and detector.dtnum:
                if Password == enteredPassword:
                    enteredPassword = ""
                    Password = None
                    oled_control(['Enter Password:', 'Pass'])
                    operate_motor()
                    logger.info("大門已開啟")
                    print("密碼正確，大門已開啟")
                else:
                    enteredPassword = ""
                    errorCount -= 1
                    print("密碼錯誤，大門未動作")
                    oled_control(['Enter Password:', 'Fail'])
                    logger.info("密碼錯誤")
                    if not errorCount:
                        Password = None
                        errorCount = 3
                        print("錯誤次數過多，已重置密碼")
                        logger.warning("密碼錯誤，已重置")
        else:
            oled_control(['No Password', 'Set Password'])
            print("密碼不存在 請設定密碼")

        if validityTime and time.time() - start_validityTime >= validityTime:
            Password = None
            logger.info("密碼時效性結束")
            print("密碼失效，密碼已清除")

        time.sleep(detection_Interval) # 限制設定的偵測間隔時間

def set_logger(): # log系統
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss} | '
        '{level} | <{module}>:{function}:{line} | '
        '{message}'
    )
    logger.add(
        './logs/system.log',
        rotation='7 day',
        retention='30 days',
        level='INFO',
        encoding='UTF-8',
        format=log_format
    )


if __name__ == '__main__':
    set_logger()
    threading.Thread(target=detector.capture_gesture, args=(cv2_Screen,)).start() # 啟動偵測手勢的線程
    threading.Thread(target=main).start() # 啟動判定的線程
    app.run(host='0.0.0.0',port=8080) # 啟動Flask
