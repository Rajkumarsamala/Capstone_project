# Virtual Control Hub

Virtual Control Hub is a next-generation desktop application that allows you to control your PC completely hands-free. By leveraging advanced Computer Vision and Voice Recognition, it translates your hand gestures and voice commands into direct desktop actions like moving the mouse, clicking, scrolling, typing, and adjusting system settings.

## 📥 Installation

No complex setup is required! 
You can download the ready-to-use Windows Executable (.exe) directly from the project website or the GitHub Releases page.

**👉 [Download Virtual Control Hub (.EXE)](https://rajkumarsamala.github.io/Capstone_project/)**

## 🖐️ Hand Gesture Controls

Use your computer's webcam to interact with your desktop using the following intuitive hand gestures:

| Action | Hand Gesture | Description |
| :--- | :--- | :--- |
| **Move Mouse** | ☝️ **Index Finger Up** | Keep your index finger pointing up (and middle finger down). Move your hand to move the cursor. |
| **Left Click** | 🤏 **Pinch Thumb & Index** | Pinch your index finger and thumb together briefly to trigger a mouse click. |
| **Scroll Page** | ✌️ **Index & Middle Up** | Raise both your index and middle fingers. Move your hand up to scroll up, and down to scroll down. |
| **Adjust Volume** | 🤙 **Pinky Up + Pinch** | Raise your pinky finger. While it's up, pinch and stretch your thumb and index finger to change the volume. |
| **Adjust Brightness**| 🖖 **Pinky & Ring Up + Pinch** | Raise your pinky and ring fingers. Pinch and stretch your thumb and index finger to change screen brightness. |

## 🎙️ Voice Commands

The system features an always-listening voice assistant. Simply say the wake word **"assistant"** to activate it, followed by your command.

| Command | Description |
| :--- | :--- |
| **"assistant"** | Wakes up the voice engine. It will reply "How can I help you?". |
| **"open notepad"** | Launches the Windows Notepad application. |
| **"open calculator"** | Launches the Windows Calculator. |
| **"open browser"** | Opens your default web browser to Google.com. |
| **"type [your text]"** | Automatically types the text you dictate. *(e.g., "type hello world")* |
| **"enter"** | Presses the 'Enter' key on your keyboard. |
| **"sleep"** | Puts the voice assistant back to sleep so it stops listening. |

## 🛠️ Technology Stack
- **Python**: Core logic
- **OpenCV & MediaPipe**: Hand tracking and gesture recognition
- **SpeechRecognition & pyttsx3**: Voice capture and text-to-speech
- **PyAutoGUI**: System-level hardware control
- **CustomTkinter**: Modern Graphical User Interface

## 🚀 Running from Source
If you want to run the python code directly instead of the `.exe`:
1. Clone the repository: `git clone https://github.com/Rajkumarsamala/Capstone_project.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

---
*Created as a Capstone Project exploring hands-free human-computer interaction.*
