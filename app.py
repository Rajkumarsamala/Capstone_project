import customtkinter as ctk
from PIL import Image
import cv2
import threading
from core.gesture_engine import GestureEngine
from core.voice_engine import VoiceEngine

class CapstoneApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Capstone: Virtual Control Hub")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Camera Frame
        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.video_label = ctk.CTkLabel(self.video_frame, text="Click Start to Launch Camera")
        self.video_label.pack(expand=True, fill="both")
        
        # Controls Frame
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.control_frame, text="System Controls", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(self.control_frame, text="▶ Start System", command=self.start_system, fg_color="#28a745", hover_color="#218838")
        self.start_btn.pack(pady=10)
        
        self.stop_btn = ctk.CTkButton(self.control_frame, text="⏹ Stop System", command=self.stop_system, fg_color="#dc3545", hover_color="#c82333", state="disabled")
        self.stop_btn.pack(pady=10)
        
        # Logs
        self.log_label = ctk.CTkLabel(self.control_frame, text="Voice Logs:", font=("Arial", 16, "bold"))
        self.log_label.pack(pady=(20, 0), anchor="w", padx=10)
        
        self.log_textbox = ctk.CTkTextbox(self.control_frame, width=300, height=300, state="disabled")
        self.log_textbox.pack(pady=5, padx=10, fill="both", expand=True)
        self.update_log("System: Ready to start.\n")
        
        # Instructions Tab or Text
        self.instr_label = ctk.CTkLabel(self.control_frame, text="Gestures:\n• Move: Index Finger Up\n• Click: Pinch Thumb & Index\n• Scroll: Index & Middle Up\n• Volume: OK Sign\n• Brightness: Fist Pinch\n• Show Desktop: Open Palm\n• Switch App: Rock Sign\n• Screenshot: Three Fingers Up", justify="left", font=("Arial", 12))
        self.instr_label.pack(pady=20, anchor="w", padx=10)
        
        # Engines
        self.gesture_engine = GestureEngine(frame_callback=self.update_video)
        self.voice_engine = VoiceEngine(log_callback=self.update_log)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def start_system(self):
        threading.Thread(target=self.gesture_engine.start, daemon=True).start()
        self.voice_engine.start()
        
        self.update_log("System: All engines started.")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
    def stop_system(self):
        self.gesture_engine.stop()
        self.voice_engine.stop()
        
        self.update_log("System: All engines stopped.")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.video_label.configure(image="")
        self.video_label.text = "Camera Stopped"
        
    def update_video(self, img_bgr):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_rgb)
        
        # Resize safely based on frame size
        frame_width = self.video_frame.winfo_width()
        frame_height = self.video_frame.winfo_height()
        if frame_width > 10 and frame_height > 10:
            pil_image = pil_image.resize((frame_width - 10, frame_height - 10), Image.Resampling.LANCZOS)
            
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
        self.video_label.configure(image=ctk_image, text="")
        self.video_label.image = ctk_image
        
    def update_log(self, text):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{text}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")
        
    def on_closing(self):
        self.stop_system()
        self.destroy()

if __name__ == "__main__":
    app = CapstoneApp()
    app.mainloop()
