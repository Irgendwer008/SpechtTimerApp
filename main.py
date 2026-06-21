#!/usr/bin/env python3

from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import time
import csv

from classes import Session, Lap
from helper import format_time

class RaceTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Race Coordinator Timer")

        self.running = False
        self.start_time = None

        self.session = Session(["Start", "Nase", "Schikane", "Norman-Kurve", "Felix-Kurve", "Shell-S"])

        info = [
            "+ = Next Checkpoint",
            "- = Retake last Checkpoint",
            "R = Reset and start new Session"
            "X = Export CSV",
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
        columns.extend(self.session.checkpoints)

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


        root.bind("<Key>", self.key_pressed)

        self.update_timer()

    def key_pressed(self, event):
        key = event.keysym.lower()

        if key == "r":
            self.start_session()
            summary = self.session.next_checkpoint()
            print(summary)
            self.add_table_entry(summary)

        elif key == "+":
            summary = self.session.next_checkpoint()
            print(summary)
            self.add_table_entry(summary)

        elif key == "-":
            summary = self.session.redo_checkpoint()
            self.add_table_entry(summary)

        elif key == "x":
            self.export_csv()

    def start_session(self):
        self.session.start()

        for row in self.table.get_children():
            self.table.delete(row)

    def update_timer(self):
        if self.session.start_time != None:
            t = self.session.elapsed()
            self.timer_label.config(text = format_time(t))
        
        self.root.after(20, self.update_timer)

    def add_table_entry(self, summary: str):
        pass







    def update_table(self, lap, checkpoint, lap_time, delta=None):

        if lap not in self.lap_data:
            self.lap_data[lap] = {}

        if delta is None:
            text = f"{lap_time:.3f}"
        else:
            text = f"{lap_time:.3f} ({delta:+.3f})"

        self.lap_data[lap][checkpoint] = text

        values = [lap]

        for cp in ["Start/Ziel"] + self.checkpoints:
            values.append(
                self.lap_data[lap].get(cp, "")
            )

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