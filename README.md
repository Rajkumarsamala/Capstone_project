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
| **Move Mouse** | ☝️ **Index Finger Up** | Keep your index finger pointing up (all other fingers down). Move your hand to move the cursor. |
| **Left Click** | 🤏 **Pinch Thumb & Index** | Pinch your index finger and thumb together briefly while pointing to trigger a mouse click. |
| **Scroll Page** | ✌️ **Peace Sign** | Raise both your index and middle fingers (others down). Move your hand up to scroll up, and down to scroll down. |
| **Adjust Volume** | 👌 **OK Sign (Pinch)** | Keep your Middle, Ring, and Pinky fingers UP (Index down). Pinch and stretch your thumb and index finger to change the volume. |
| **Adjust Brightness**| ✊ **Fist Pinch (Salt)** | Keep your Middle, Ring, and Pinky fingers DOWN (curled in). Pinch and stretch your thumb and index finger to change screen brightness. |
| **Show Desktop** | 🖐️ **Open Palm** | Raise all five fingers open to minimize all windows and show the desktop. |
| **Switch App** | 🤘 **Rock Sign** | Raise only your Index and Pinky fingers to quickly switch to the previous application. |
| **Take Screenshot**| 🖖 **Three Fingers Up**| Raise your Index, Middle, and Ring fingers (Pinky down) to take a full-screen screenshot. |

## 🎙️ Voice Commands

The system features an always-listening voice assistant. Simply say the wake word **"assistant"** to activate it, followed by your command.

| Command | Description |
| :--- | :--- |
| **"assistant"** | Wakes up the voice engine. It will reply "How can I help you?". |
| **"open notepad"** | Launches the Windows Notepad application. |
| **"open calculator"** | Launches the Windows Calculator. |
| **"open browser"** | Opens your default web browser to Google.com. |
| **"close window"** | Closes the currently active application window. |
| **"copy that"** | Copies the currently selected text or item. |
| **"paste that"** | Pastes the copied text or item. |
| **"select all"** | Selects all text or items in the active window. |
| **"undo"** | Undoes your last action. |
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
