import speech_recognition as sr
import os
import pyautogui
import threading
import pyttsx3
import datetime
import webbrowser
class VoiceEngine:
    def __init__(self, log_callback=None):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        
        self.running = False
        self.log_callback = log_callback 
        self.is_awake = False
        self.wake_word = "assistant"

    def speak(self, text):
        def _speak():
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.say(text)
            engine.runAndWait()
        threading.Thread(target=_speak, daemon=True).start()

    def log(self, text):
        if self.log_callback:
            self.log_callback(text)
        else:
            print(text)

    def start(self):
        self.running = True
        threading.Thread(target=self._listen_loop, daemon=True).start()
        
    def stop(self):
        self.running = False
        
    def _listen_loop(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.log(f"System: Voice Engine Ready. Say '{self.wake_word}' to wake.")
            
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    self.log(f"You: {command}")
                    self._process_command(command)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    pass

    def _process_command(self, command):
        if self.wake_word in command:
            if not self.is_awake:
                self.is_awake = True
                self.speak("How can I help you?")
                self.log("System: Assistant is AWAKE")
            
            command = command.replace(self.wake_word, "").strip()
            if not command:
                return
            
        if not self.is_awake:
            return
            
        if "sleep" in command or "stop listening" in command:
            self.is_awake = False
            self.speak("Going to sleep.")
            self.log("System: Assistant went to SLEEP")
            return
            
        if "open notepad" in command:
            self.speak("Opening Notepad")
            os.system("notepad")
        elif "open calculator" in command:
            self.speak("Opening Calculator")
            os.system("calc")
        elif "browser" in command and "open" in command:
            self.speak("Opening Browser")
            webbrowser.open("https://www.google.com")
        elif "search for" in command:
            query = command.split("search for", 1)[1].strip()
            self.speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "what time is it" in command or "current time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
            self.log(f"System: Time is {now}")
        elif "what is the date" in command or "today's date" in command:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")
            self.log(f"System: Date is {today}")
        elif "open file explorer" in command or "open explorer" in command:
            self.speak("Opening File Explorer")
            os.system("explorer")
        elif "recycle bin" in command:
            self.speak("Opening Recycle Bin")
            os.system("start shell:RecycleBinFolder")
        elif "open command prompt" in command or "open cmd" in command:
            self.speak("Opening Command Prompt")
            os.system("start cmd")
        elif "maximize window" in command:
            self.speak("Maximizing window")
            pyautogui.hotkey("win", "up")
        elif "minimize window" in command:
            self.speak("Minimizing window")
            pyautogui.hotkey("win", "down")
        elif "switch window" in command:
            self.speak("Switching window")
            pyautogui.hotkey("alt", "tab")
        elif "show desktop" in command or "go to desktop" in command:
            self.speak("Showing desktop")
            pyautogui.hotkey("win", "d")
        elif "volume up" in command:
            self.speak("Increasing volume")
            for _ in range(5):
                pyautogui.press("volumeup")
        elif "volume down" in command:
            self.speak("Decreasing volume")
            for _ in range(5):
                pyautogui.press("volumedown")
        elif "mute volume" in command or "unmute volume" in command:
            self.speak("Toggling mute")
            pyautogui.press("volumemute")
        elif "type" in command:
            text = command.split("type", 1)[1].strip()
            self.speak(f"Typing: {text}")
            pyautogui.write(text, interval=0.05)
        elif "enter" in command:
            pyautogui.press("enter")
        elif "close window" in command:
            self.speak("Closing window")
            pyautogui.hotkey("alt", "f4")
        elif "copy that" in command or "copy text" in command:
            self.speak("Copied")
            pyautogui.hotkey("ctrl", "c")
        elif "paste that" in command or "paste text" in command:
            self.speak("Pasted")
            pyautogui.hotkey("ctrl", "v")
        elif "select all" in command:
            self.speak("Selected all")
            pyautogui.hotkey("ctrl", "a")
        elif "undo" in command:
            self.speak("Undoing")
            pyautogui.hotkey("ctrl", "z")
