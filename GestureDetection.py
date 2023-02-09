import cv2, math
import mediapipe as mp
from enum import Enum

class Finger(Enum): # 大拇指、食指、中指、無名指、小指
    THUMB = (0, 2, 3, 4)
    INDEX = (0, 6, 7, 8)
    MIDDLE = (0, 10, 11, 12)
    RING = (0, 14, 15, 16)
    PINKY = (0, 18, 19, 20)

class GestureDetector:
    def __init__(self):
        self.dtnum = None
        self.gestures = {
            # 以下可以自由新增，或更改
            # 依序為：大拇指、食指、中指、無名指、小指
            # 0 代表 手指折起來 
            # 1 代表伸直 
            (0, 0, 0, 0, 0): '0',
            (0, 1, 0, 0, 0): '1',
            (0, 1, 1, 0, 0): '2',
            (0, 1, 1, 1, 0): '3',
            (0, 1, 1, 1, 1): '4',
            (1, 1, 1, 1, 1): '5',
            (1, 0, 0, 0, 1): '6',
            (1, 1, 0, 0, 0): '7',
            (1, 1, 1, 0, 0): '8',
            (1, 1, 1, 1, 0): '9',
            (1, 0, 0, 0, 0): 'Great',
        }

    def angle_between_vectors(self, v1, v2):
        v1_x, v1_y = v1
        v2_x, v2_y = v2
        try:
            angle_ = math.degrees(math.acos((v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
        except:
            angle_ = 65535
        if angle_ > 180:
            angle_ = 65535
        return angle_

    def finger_angles(self, hand_points):
        angle_list = []
        for finger in Finger:
            angle_ = self.angle_between_vectors(
                ((int(hand_points[finger.value[0]][0]) - int(hand_points[finger.value[1]][0])), (int(hand_points[finger.value[0]][1]) - int(hand_points[finger.value[1]][1]))),
                ((int(hand_points[finger.value[2]][0]) - int(hand_points[finger.value[3]][0])), (int(hand_points[finger.value[2]][1]) - int(hand_points[finger.value[3]][1])))
            )
            angle_list.append(angle_)
        return angle_list

    def reco_gesture(self, angle_list):
        thr_angle = 49 
        # thr_angle 是手指角度的閥值，用來判斷手指是不是伸直的，
        # 若手指的角度小於 thr_angle ，則判定為伸直，反之會是折起，若效果不太好可以選擇微調喔。
        gesture = [1 if angle < thr_angle else 0 for angle in angle_list]
        return self.gestures.get(tuple(gesture), None)

    def capture_gesture(self, Screen=False):
        # 初始化 MediaPipe Hands pipeline 以進行手部辨識
        hands_pipeline = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)
        # 啟動並抓取第一個 webcam , 若你用多個 Webcam 可以調整此值 
        cap = cv2.VideoCapture(0)
        while True:
            # 讀取 webcam 的 Frame
            ret,frame = cap.read() # 如果有畫面，那麼 ret 會是 True 相對無畫面的話 會是 False
            if not ret:
                raise Exception("無法檢測到攝像頭，請確認攝像頭是否已經正確連接並開啟")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            # 利用 MediaPipe Hands 進行手部辨識
            results = hands_pipeline.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 在影像上繪製手部的特徵點
                    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                    hand_local = []
                    for i in range(21):
                        x = hand_landmarks.landmark[i].x*frame.shape[1]
                        y = hand_landmarks.landmark[i].y*frame.shape[0]
                        hand_local.append((x,y))
                    if hand_local:
                        angle_list = self.finger_angles(hand_local)
                        gesture_str = self.reco_gesture(angle_list)
                        self.dtnum = gesture_str
                        cv2.putText(frame,gesture_str,(0,100),0,1.3,(0,0,255),3)
            else:
                self.dtnum = None
            if Screen:
                cv2.imshow('MediaPipe Hands', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()

if __name__ == '__main__': # 單獨啟動此程式預留用的
    detector = GestureDetector()
    detector.capture_gesture(Screen=True)