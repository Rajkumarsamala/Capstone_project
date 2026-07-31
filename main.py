import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import threading
import math
import numpy as np
import time
import os

# PyAutoGUI settings
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

class VirtualController:
    def __init__(self):
        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        
        # State
        self.running = True
        self.click_cooldown = 0
        self.prev_x, self.prev_y = 0, 0
        self.smoothing = 5
        self.scroll_start_y = 0
        
    def listen_voice(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for voice commands...")
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"Command: {command}")
                    self.execute_command(command)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    pass

    def execute_command(self, command):
        print(f"Executing: {command}")
        if "open notepad" in command:
            os.system("notepad")
        elif "open calculator" in command:
            os.system("calc")
        elif "open browser" in command:
            os.system("start https://www.google.com")
        elif "type" in command:
            text = command.split("type", 1)[1].strip()
            pyautogui.write(text, interval=0.05)
        elif "enter" in command:
            pyautogui.press("enter")
        elif "close program" in command or "stop program" in command:
            self.running = False

    def run(self):
        # Start voice listening in a separate thread
        threading.Thread(target=self.listen_voice, daemon=True).start()
        
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        
        while self.running and cap.isOpened():
            success, img = cap.read()
            if not success:
                break
                
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    lmList = []
                    h, w, c = img.shape
                    for id, lm in enumerate(hand_landmarks.landmark):
                        lmList.append([id, int(lm.x * w), int(lm.y * h)])
                        
                    if len(lmList) > 0:
                        x1, y1 = lmList[8][1:]  # Index
                        x2, y2 = lmList[12][1:] # Middle
                        tx, ty = lmList[4][1:]  # Thumb
                        
                        fingers = []
                        # 4 Fingers (Index, Middle, Ring, Pinky)
                        for id in range(8, 21, 4):
                            fingers.append(1 if lmList[id][2] < lmList[id-2][2] else 0)
                            
                        # Move Mouse (Index Up, Middle Down)
                        if fingers[0] == 1 and fingers[1] == 0:
                            frame_margin = 100
                            cv2.rectangle(img, (frame_margin, frame_margin), (w - frame_margin, h - frame_margin), (255, 0, 255), 2)
                            
                            x3 = np.interp(x1, (frame_margin, w - frame_margin), (0, SCREEN_WIDTH))
                            y3 = np.interp(y1, (frame_margin, h - frame_margin), (0, SCREEN_HEIGHT))
                            
                            curr_x = self.prev_x + (x3 - self.prev_x) / self.smoothing
                            curr_y = self.prev_y + (y3 - self.prev_y) / self.smoothing
                            
                            try:
                                pyautogui.moveTo(curr_x, curr_y)
                            except:
                                pass
                                
                            self.prev_x, self.prev_y = curr_x, curr_y
                            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                            
                        # Scroll (Index and Middle Up, Ring Down)
                        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
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
                            
                        # Click (Pinch Thumb and Index)
                        dist = math.hypot(tx - x1, ty - y1)
                        if dist < 30:
                            if time.time() > self.click_cooldown:
                                cv2.circle(img, (tx, ty), 15, (0, 255, 0), cv2.FILLED)
                                pyautogui.click()
                                self.click_cooldown = time.time() + 0.5

            cv2.putText(img, "Index: Move | Index+Middle: Scroll | Pinch: Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(img, "Voice: 'open notepad', 'type <text>', 'close program'", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            cv2.imshow("Virtual Control", img)
            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = VirtualController()
    app.run()
