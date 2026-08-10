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
            
        if "sleep" in command or "stop" in command:
            self.is_awake = False
            self.speak("Going to sleep.")
            self.log("System: Assistant went to SLEEP")
            return
            
        if "notepad" in command:
            self.speak("Opening Notepad")
            os.system("notepad")
        elif "calculator" in command or "calc" in command:
            self.speak("Opening Calculator")
            os.system("calc")
        elif "browser" in command or "google" in command:
            self.speak("Opening Browser")
            webbrowser.open("https://www.google.com")
        elif "search" in command:
            query = command.replace("search for", "").replace("search", "").strip()
            if query:
                self.speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "calculate" in command or "what is" in command or "how much is" in command:
            try:
                expression = command.replace("calculate", "").replace("what is", "").replace("how much is", "")
                expression = expression.replace("x", "*").replace("into", "*").replace("times", "*").replace("multiplied by", "*")
                expression = expression.replace("plus", "+").replace("and", "+")
                expression = expression.replace("minus", "-").replace("take away", "-")
                expression = expression.replace("divided by", "/").replace("over", "/")
                
                allowed_chars = "0123456789+-*/.() "
                cleaned_expr = "".join(c for c in expression if c in allowed_chars).strip()
                
                if cleaned_expr:
                    result = eval(cleaned_expr)
                    self.speak(f"The answer is {result}")
                    self.log(f"System: Calculated {cleaned_expr} = {result}")
                else:
                    self.speak("I couldn't understand the math.")
            except Exception:
                self.speak("Sorry, I couldn't calculate that.")
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
            self.log(f"System: Time is {now}")
        elif "date" in command:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")
            self.log(f"System: Date is {today}")
        elif "explorer" in command or "file manager" in command or "files" in command:
            self.speak("Opening File Explorer")
            os.system("explorer")
        elif "recycle bin" in command or "trash" in command:
            self.speak("Opening Recycle Bin")
            os.system("start shell:RecycleBinFolder")
        elif "cmd" in command or "command prompt" in command or "terminal" in command:
            self.speak("Opening Command Prompt")
            os.system("start cmd")
        elif "maximize" in command:
            self.speak("Maximizing window")
            pyautogui.hotkey("win", "up")
        elif "minimize" in command:
            self.speak("Minimizing window")
            pyautogui.hotkey("win", "down")
        elif "switch" in command:
            self.speak("Switching window")
            pyautogui.hotkey("alt", "tab")
        elif "desktop" in command:
            self.speak("Showing desktop")
            pyautogui.hotkey("win", "d")
        elif "volume" in command and "up" in command or "increase" in command and "volume" in command:
            self.speak("Increasing volume")
            for _ in range(5):
                pyautogui.press("volumeup")
        elif "volume" in command and "down" in command or "decrease" in command and "volume" in command:
            self.speak("Decreasing volume")
            for _ in range(5):
                pyautogui.press("volumedown")
        elif "mute" in command or "silence" in command:
            self.speak("Toggling mute")
            pyautogui.press("volumemute")
        elif "type" in command:
            try:
                text = command.split("type", 1)[1].strip()
                self.speak(f"Typing: {text}")
                pyautogui.write(text, interval=0.05)
            except IndexError:
                pass
        elif "enter" in command or "return" in command:
            pyautogui.press("enter")
        elif "close" in command and "window" in command or "exit" in command:
            self.speak("Closing window")
            pyautogui.hotkey("alt", "f4")
        elif "copy" in command:
            self.speak("Copied")
            pyautogui.hotkey("ctrl", "c")
        elif "paste" in command:
            self.speak("Pasted")
            pyautogui.hotkey("ctrl", "v")
        elif "select all" in command:
            self.speak("Selected all")
            pyautogui.hotkey("ctrl", "a")
        elif "undo" in command:
            self.speak("Undoing")
            pyautogui.hotkey("ctrl", "z")
