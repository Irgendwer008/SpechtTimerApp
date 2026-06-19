#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import time
import csv
from datetime import datetime

class RaceTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Race Coordinator Timer")

        self.running = False
        self.start_time = None
        self.lap_number = 1
        self.events = []

        self.checkpoints = ["Nase", "Schikane", "Norman-Kurve", "Felix-Kurve", "Shell-S"]

        self.timer_label = tk.Label(
            root,
            text="00:00.000",
            font=("Arial", 40),
        )
        self.timer_label.pack(pady=20)

        info = [
            "S = Start/Ziel",
            "1 = Nase",
            "2 = Schikane",
            "3 = Norman-Kurve",
            "4 = Felix-Kurve",
            "5 = Shell-S",
            "SPACE = Finish Lap",
            "X = Export CSV",
        ]

        for line in info:
            tk.Label(root, text=line, font=("Arial", 16)).pack()

        self.log = tk.Text(root, height=15, width=80)
        self.log.pack(pady=20)

        root.bind("<Key>", self.key_pressed)

        self.update_timer()

    def key_pressed(self, event):
        key = event.keysym.lower()

        if key == "s":
            self.start_session()

        elif key == "space":
            self.record_event("Start/Ziel")
            self.lap_number += 1

        elif key == "x":
            self.export_csv()

        else:
            try:
                number = int(key) - 1
                if number in range(0, len(self.checkpoints)):
                    self.record_event(self.checkpoints[number])
            except:
                pass

    def start_session(self):
        self.running = True
        self.start_time = time.perf_counter()
        self.lap_number = 1
        self.events.clear()
        self.log.delete("1.0", tk.END)

        self.log.insert(
            tk.END,
            f"Session started at {datetime.now()}\n\n"
        )

    def elapsed(self):
        if not self.running:
            return 0.0
        return time.perf_counter() - self.start_time

    def record_event(self, checkpoint):
        if not self.running:
            return

        t = self.elapsed()

        self.events.append({
            "lap": self.lap_number,
            "checkpoint": checkpoint,
            "time": round(t, 3)
        })

        print(self.events)

        self.log.insert(
            tk.END,
            f"Lap {self.lap_number:02d} | "
            f"{checkpoint:<12} | "
            f"{t:.3f}s\n"
        )

        self.log.see(tk.END)

    def update_timer(self):
        if self.running:
            t = self.elapsed()
            minutes = int(t // 60)
            seconds = t % 60

            self.timer_label.config(
                text=f"{minutes:02d}:{seconds:06.3f}"
            )

        self.root.after(20, self.update_timer)

    def export_csv(self):
        if not self.events:
            messagebox.showinfo("Info", "No events recorded.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv"
        )

        if not filename:
            return

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["lap", "checkpoint", "time"]
            )

            writer.writeheader()
            writer.writerows(self.events)

        messagebox.showinfo(
            "Saved",
            f"Exported {len(self.events)} events."
        )

root = tk.Tk()
root.geometry("1200x900")
app = RaceTimer(root)
root.mainloop()