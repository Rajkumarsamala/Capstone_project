import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

pyautogui.FAILSAFE = False

class GestureEngine:
    def __init__(self, frame_callback=None):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        self.frame_callback = frame_callback
        self.running = False
        
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        self.smoothing = 5
        self.click_cooldown = 0
        self.action_cooldown = 0
        self.scroll_start_y = 0
        
        # Audio setup
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)
            self.vol_range = self.volume.GetVolumeRange()
            self.min_vol, self.max_vol = self.vol_range[0], self.vol_range[1]
        except Exception:
            self.volume = None

    def start(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        
        while self.running and self.cap.isOpened():
            success, img = self.cap.read()
            if not success:
                continue
                
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self._process_gestures(hand_landmarks.landmark, img)
                    
            if self.frame_callback:
                self.frame_callback(img)
            else:
                cv2.imshow("Gesture Control", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        if self.cap:
            self.cap.release()
            
    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
        
    def _process_gestures(self, landmarks, img):
        h, w, c = img.shape
        lmList = [[id, int(lm.x * w), int(lm.y * h)] for id, lm in enumerate(landmarks)]
        
        x1, y1 = lmList[8][1:]  # Index tip
        x2, y2 = lmList[12][1:] # Middle tip
        tx, ty = lmList[4][1:]  # Thumb tip
        
        fingers = []
        for id in range(8, 21, 4):
            fingers.append(1 if lmList[id][2] < lmList[id-2][2] else 0)
            
        # 1. Volume Control: OK Sign (Middle, Ring, Pinky UP, Index DOWN)
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and self.volume:
            dist = math.hypot(tx - x1, ty - y1)
            cv2.line(img, (tx, ty), (x1, y1), (255, 0, 0), 3)
            vol = np.interp(dist, [20, 150], [self.min_vol, self.max_vol])
            try: self.volume.SetMasterVolumeLevel(vol, None)
            except: pass
            
        # 2. Brightness Control: Fist Pinch (All fingers DOWN / curled)
        elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0:
            dist = math.hypot(tx - x1, ty - y1)
            cv2.line(img, (tx, ty), (x1, y1), (0, 255, 255), 3)
            bright = np.interp(dist, [20, 150], [0, 100])
            try: sbc.set_brightness(int(bright))
            except: pass
            
        # 3. Scroll: Peace Sign (Index & Middle UP, Ring & Pinky DOWN)
        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
            cy = (y1 + y2) // 2
            if self.scroll_start_y == 0:
                self.scroll_start_y = cy
            else:
                if cy < self.scroll_start_y - 20:
                    pyautogui.scroll(100) # Up
                    self.scroll_start_y = cy
                elif cy > self.scroll_start_y + 20:
                    pyautogui.scroll(-100) # Down
                    self.scroll_start_y = cy
        else:
            self.scroll_start_y = 0

        # 5. Show Desktop: All Fingers UP (Open Palm)
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            if time.time() > self.action_cooldown:
                pyautogui.hotkey('win', 'd')
                self.action_cooldown = time.time() + 1.0

        # 6. Switch Window: Index and Pinky UP (Rock Sign)
        elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 1:
            if time.time() > self.action_cooldown:
                pyautogui.hotkey('alt', 'tab')
                self.action_cooldown = time.time() + 1.0

        # 7. Screenshot: Index, Middle, Ring UP (Three Fingers)
        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            if time.time() > self.action_cooldown:
                pyautogui.hotkey('win', 'prtscr')
                self.action_cooldown = time.time() + 2.0
            
            
        # 4. Mouse Move: Pointing (ONLY Index UP, Middle, Ring, Pinky DOWN)
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0:
            frame_margin = 100
            cv2.rectangle(img, (frame_margin, frame_margin), (w - frame_margin, h - frame_margin), (255, 0, 255), 2)
            
            x3 = np.interp(x1, (frame_margin, w - frame_margin), (0, self.screen_w))
            y3 = np.interp(y1, (frame_margin, h - frame_margin), (0, self.screen_h))
            
            curr_x = self.prev_x + (x3 - self.prev_x) / self.smoothing
            curr_y = self.prev_y + (y3 - self.prev_y) / self.smoothing
            
            try: pyautogui.moveTo(curr_x, curr_y)
            except: pass
            
            self.prev_x, self.prev_y = curr_x, curr_y
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            
            # Click (Pinch Thumb and Index)
            dist = math.hypot(tx - x1, ty - y1)
            if dist < 30 and time.time() > self.click_cooldown:
                cv2.circle(img, (tx, ty), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                self.click_cooldown = time.time() + 0.5
