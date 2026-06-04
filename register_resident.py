import tkinter as tk
from tkinter import messagebox
import json
import os

def save_resident():

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    risk = risk_var.get()

    if not name or not age:
        messagebox.showerror(
            "Error",
            "Please complete all fields"
        )
        return

    try:
        with open("residents.json", "r") as f:
            residents = json.load(f)
    except:
        residents = []

    residents.append({
        "name": name,
        "age": age,
        "risk_level": risk
    })

    with open("residents.json", "w") as f:
        json.dump(residents, f, indent=4)

    messagebox.showinfo(
        "Success",
        "Resident registered successfully"
    )

    root.destroy()

root = tk.Tk()

root.title("Register Resident")
root.geometry("350x250")

tk.Label(root, text="Name").pack(pady=5)

name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Age").pack(pady=5)

age_entry = tk.Entry(root, width=30)
age_entry.pack()

tk.Label(root, text="Risk Level").pack(pady=5)

risk_var = tk.StringVar(value="Low")

risk_menu = tk.OptionMenu(
    root,
    risk_var,
    "Low",
    "Medium",
    "High"
)

risk_menu.pack()

tk.Button(
    root,
    text="Save Resident",
    command=save_resident
).pack(pady=20)

root.mainloop()