#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import time
import csv

from classes import Session, Lap
from helper import format_time

checkpoints = ["Nase", "Schikane", "Norman-Kurve", "Felix-Kurve", "Shell-S #1", "Shell-S #2", "Start / Ziel"]

class RaceTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Race Coordinator Timer")

        self.running = False
        self.start_time = None
        self.current_table_row_texts = []

        info = [
            "+ = Next Checkpoint",
            "- = Retake last Checkpoint",
            "R = Reset and start new Session",
            "Ctrl + S = Export CSV",
            "Ctrl + Q = Quit Program"
        ]

        self.timer_label = tk.Label(
            root,
            text="00:00.000",
            font=("Arial", 40),
        )
        self.timer_label.pack(pady=20)

        self.diff_label = tk.Label(
            root,
            text="00:00.000",
            font=("Arial", 30),
        )
        self.diff_label.pack(pady=20)

        for line in info:
            tk.Label(root, text=line, font=("Arial", 16)).pack()

        # Table

        columns = ["Lap"]
        columns.extend(checkpoints)

        self.table = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=20
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=160, anchor="center")

        self.table.pack(fill="both", expand=True, padx=20, pady=20)

        self.start_session(checkpoints)

        root.bind("<Key>", self.key_pressed)
        root.bind("<Control-q>", self.quit)
        root.bind("<Control-s>", self.export_csv)

    def quit(self, _ = None):
        self.root.destroy()

    def key_pressed(self, event):
        key = event.keysym.lower()

        match key:
            case "r":
                self.start_session(checkpoints)

                self.update_timer()
                self.running = True

            case "+":
                if self.running:
                    summary, diff_time = self.session.next_checkpoint()
                    self.update_diff_label(diff_time)
                    self.add_table_entry(summary)
                else:
                    self.start_session(checkpoints)

                    self.update_timer()
                    self.running = True


            case "-":
                if self.running:
                    summary, diff_time = self.session.redo_checkpoint()
                    self.update_diff_label(diff_time)

                    if len(self.session.laps[-1].relative_checkpoint_times) == 0:
                        last_row = self.table.get_children()[-1]
                        self.current_table_row_texts = self.table.item(last_row)["values"][1:-1] # remove first entry wich is lap number
                    else:
                        self.current_table_row_texts.pop()

                    self.add_table_entry(summary)
            
    def start_session(self, checkpoints: list[str]):
        self.current_table_row_texts = []
        self.diff_label.config(text="00:00.000")
        
        self.session = Session(checkpoints)
        self.session.start()

        for row in self.table.get_children():
            self.table.delete(row)

    def update_timer(self):
        if self.session.start_time != None:
            t = self.session.elapsed()
            self.timer_label.config(text = format_time(t))
        
        self.root.after(20, self.update_timer)

    def add_table_entry(self, summary: str):
        lap = len(self.session.laps)

        # reset if new line (= new lap)
        if len(self.session.laps[-1].relative_checkpoint_times) == 0:
            lap -= 1
        
        self.current_table_row_texts.append(summary)
        values = [str(lap)]
        values.extend(self.current_table_row_texts)

        item_id = f"lap_{lap}"

        if self.table.exists(item_id):
            self.table.item(item_id, values=values)
        else:
            self.table.insert(
                "",
                "end",
                iid=item_id,
                values=values
            )

        if len(values) > len(self.session.checkpoints):
            self.current_table_row_texts = []
    
    def update_diff_label(self, diff_time: float):
        if diff_time is None:
            return
        elif diff_time > 0.0:
            self.diff_label.config(text=format_time(diff_time, time_diff=True), fg="red")
        else:
            self.diff_label.config(text=format_time(diff_time, time_diff=True), fg="green")

    def export_csv(self, _ = None):
        if self.session.laps == []:
            messagebox.showinfo("Info", "No events recorded.")
            return

        with open(Path.home() / "Downloads" / f"{self.session.date.strftime("%Y-%m-%d %H:%M:%S")} (exported {datetime.now().strftime("%H:%M:%S")}).csv", "w", newline="") as f:
            writer = csv.writer(f)

            # Header
            header = ["Lap", "Lap start time"]
            header.extend(
                f"{i}" for i in self.session.checkpoints
            )
            writer.writerow(header)

            # Data
            for lap in self.session.laps:
                row = [lap.number + 1, lap.start_time]
                row.extend(lap.relative_checkpoint_times)
                writer.writerow(row)

        messagebox.showinfo(
            "Saved",
            f"Exported {len(self.session.laps)} laps."
        )

root = tk.Tk()
root.geometry("2500x1500")
app = RaceTimer(root)
root.mainloop()