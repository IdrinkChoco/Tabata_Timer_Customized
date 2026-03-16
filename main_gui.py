import tkinter as tk
from tkinter import messagebox, filedialog
from engine import TabataEngine
import os

class TabataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabata Timer by CatDrinkChoco")
        self.root.iconbitmap("logo.ico")
        self.engine = TabataEngine()
        
        # Default Assets
        self.work_alarm = "assets/alarm_kerja.mp3" if os.path.exists("assets/alarm_kerja.mp3") else ""
        self.stand_alarm = "assets/alarm_stand.mp3" if os.path.exists("assets/alarm_stand.mp3") else ""

        # State Variables
        self.work_time = tk.IntVar(value=25)
        self.stand_time = tk.IntVar(value=5)
        self.cycles = tk.IntVar(value=4)
        self.remaining_sec = 0
        self.current_cycle = 1
        self.timer_running = False
        self.is_paused = False
        self.current_phase = "KERJA"

        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.root, padx=20, pady=20)
        container.pack()

        # Inputs
        tk.Label(container, text="Menit Kerja:").grid(row=0, column=0, sticky="w")
        tk.Entry(container, textvariable=self.work_time, width=10).grid(row=0, column=1)
        tk.Label(container, text="Menit Berdiri:").grid(row=1, column=0, sticky="w")
        tk.Entry(container, textvariable=self.stand_time, width=10).grid(row=1, column=1)
        tk.Label(container, text="Total Siklus:").grid(row=2, column=0, sticky="w")
        tk.Entry(container, textvariable=self.cycles, width=10).grid(row=2, column=1)

        # Alarm Selectors
        tk.Button(container, text="🔈 Pilih Alarm Kerja", command=lambda: self.select_file('work')).grid(row=3, column=0, pady=5)
        tk.Button(container, text="🔈 Pilih Alarm Berdiri", command=lambda: self.select_file('stand')).grid(row=3, column=1, pady=5)

        # Timer Display
        self.label_status = tk.Label(container, text="Siap Beraksi?", font=("Arial", 12, "bold"), fg="blue")
        self.label_status.grid(row=4, column=0, columnspan=2, pady=10)
        self.label_timer = tk.Label(container, text="00:00", font=("Courier", 40, "bold"))
        self.label_timer.grid(row=5, column=0, columnspan=2)

        # Control Buttons
        btn_frame = tk.Frame(container)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        self.btn_start = tk.Button(btn_frame, text="START", width=8, bg="green", fg="white", command=self.start_timer)
        self.btn_start.pack(side="left", padx=5)
        self.btn_pause = tk.Button(btn_frame, text="PAUSE", width=8, state="disabled", command=self.toggle_pause)
        self.btn_pause.pack(side="left", padx=5)
        tk.Button(btn_frame, text="STOP/RESET", width=12, bg="red", fg="white", command=self.reset_timer).pack(side="left", padx=5)

    def select_file(self, mode):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if path:
            if mode == 'work': self.work_alarm = path
            else: self.stand_alarm = path

    def toggle_pause(self):
        if self.timer_running:
            self.is_paused = not self.is_paused
            self.btn_pause.config(text="RESUME" if self.is_paused else "PAUSE")

    def reset_timer(self):
        self.timer_running = False
        self.is_paused = False
        self.current_cycle = 1
        self.engine.stop_audio()
        self.label_timer.config(text="00:00")
        self.label_status.config(text="Reset Berhasil!", fg="red")
        self.btn_start.config(state="normal")
        self.btn_pause.config(state="disabled")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.is_paused = False
            self.current_cycle = 1
            self.btn_start.config(state="disabled")
            self.btn_pause.config(state="normal")
            self.start_phase("KERJA", self.work_time.get() * 60)

    def start_phase(self, phase, seconds):
        if not self.timer_running: return
        self.current_phase = phase
        self.remaining_sec = seconds
        self.label_status.config(text=f"Siklus {self.current_cycle}: {phase}")
        self.tick()

    def tick(self):
        if not self.timer_running: return
        if not self.is_paused:
            if self.remaining_sec >= 0:
                mins, secs = divmod(self.remaining_sec, 60)
                self.label_timer.config(text=f"{mins:02d}:{secs:02d}")
                self.remaining_sec -= 1
                self.root.after(1000, self.tick)
            else:
                self.phase_done()
        else:
            self.root.after(1000, self.tick)

    def phase_done(self):
        alarm = self.work_alarm if self.current_phase == "KERJA" else self.stand_alarm
        self.engine.play_audio(alarm)
        messagebox.showinfo("Ganti Posisi!", f"Sesi {self.current_phase} Selesai!")
        self.engine.stop_audio()
        
        if self.current_phase == "KERJA":
            self.start_phase("BERDIRI", self.stand_time.get() * 60)
        else:
            self.current_cycle += 1
            if self.current_cycle <= self.cycles.get():
                self.start_phase("KERJA", self.work_time.get() * 60)
            else:
                self.reset_timer()
                messagebox.showinfo("Selesai!", "Semua siklus selesai!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TabataGUI(root)
    root.mainloop()