import tkinter as tk
from tkinter import messagebox
import json
import subprocess
import os

monitor_process = None

# -----------------------------
# LOAD RESIDENTS
# -----------------------------
def load_residents():

    try:
        with open("residents.json", "r") as f:
            return json.load(f)

    except:
        return []

# -----------------------------
# REFRESH RESIDENT LIST
# -----------------------------
def refresh_residents():

    resident_box.delete(0, tk.END)

    residents = load_residents()

    for resident in residents:

        resident_box.insert(
            tk.END,
            f"{resident['name']} | "
            f"Age: {resident['age']} | "
            f"Risk: {resident['risk_level']}"
        )

# -----------------------------
# START MONITORING
# -----------------------------
def start_monitoring():

    global monitor_process

    if monitor_process is None:

        monitor_process = subprocess.Popen(
            ["py", "-3.11", "monitoring.py"]
        )

        status_label.config(
            text="Monitoring Active"
        )

# -----------------------------
# STOP MONITORING
# -----------------------------
def stop_monitoring():

    global monitor_process

    if monitor_process:

        monitor_process.terminate()

        monitor_process = None

        status_label.config(
            text="Monitoring Stopped"
        )

# -----------------------------
# VIEW LOGS
# -----------------------------
def view_logs():

    if not os.path.exists("event_log.txt"):

        messagebox.showinfo(
            "Logs",
            "No logs found"
        )

        return

    log_window = tk.Toplevel(root)

    log_window.title("Event Logs")

    log_window.geometry("700x400")

    text = tk.Text(log_window)

    text.pack(fill="both", expand=True)

    with open("event_log.txt", "r") as f:

        text.insert("1.0", f.read())

# -----------------------------
# VIEW SCREENSHOTS
# -----------------------------
def view_screenshots():

    screenshots_folder = os.path.join(
        os.getcwd(),
        "screenshots"
    )

    if not os.path.exists(screenshots_folder):

        messagebox.showerror(
            "Error",
            "Screenshots folder not found"
        )

        return

    os.startfile(screenshots_folder)

# -----------------------------
# REGISTER RESIDENT
# -----------------------------
def register_resident():

    register_window = tk.Toplevel(root)

    register_window.title(
        "Register Resident"
    )

    register_window.geometry(
        "350x250"
    )

    tk.Label(
        register_window,
        text="Name"
    ).pack(pady=5)

    name_entry = tk.Entry(
        register_window,
        width=30
    )

    name_entry.pack()

    tk.Label(
        register_window,
        text="Age"
    ).pack(pady=5)

    age_entry = tk.Entry(
        register_window,
        width=30
    )

    age_entry.pack()

    tk.Label(
        register_window,
        text="Risk Level"
    ).pack(pady=5)

    risk_var = tk.StringVar(
        value="Low"
    )

    risk_menu = tk.OptionMenu(
        register_window,
        risk_var,
        "Low",
        "Medium",
        "High"
    )

    risk_menu.pack()

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

            with open(
                "residents.json",
                "r"
            ) as f:

                residents = json.load(f)

        except:

            residents = []

        residents.append({

            "name": name,
            "age": age,
            "risk_level": risk

        })

        with open(
            "residents.json",
            "w"
        ) as f:

            json.dump(
                residents,
                f,
                indent=4
            )

        refresh_residents()

        messagebox.showinfo(
            "Success",
            "Resident Registered"
        )

        register_window.destroy()

    tk.Button(
        register_window,
        text="Save Resident",
        command=save_resident
    ).pack(pady=20)

# -----------------------------
# EXIT APPLICATION
# -----------------------------
def exit_app():

    stop_monitoring()

    root.destroy()

# -----------------------------
# MAIN WINDOW
# -----------------------------
root = tk.Tk()

root.title(
    "Smart Home Guardian"
)

root.geometry(
    "900x600"
)

title = tk.Label(
    root,
    text="Smart Home Guardian",
    font=("Arial", 22, "bold")
)

title.pack(pady=10)

tk.Label(
    root,
    text="Registered Residents",
    font=("Arial", 14)
).pack()

resident_box = tk.Listbox(
    root,
    width=90,
    height=12
)

resident_box.pack(pady=10)

refresh_residents()

status_label = tk.Label(
    root,
    text="System Ready",
    font=("Arial", 14, "bold")
)

status_label.pack(pady=10)

button_frame = tk.Frame(root)

button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="Start Monitoring",
    width=18,
    height=2,
    command=start_monitoring
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Stop Monitoring",
    width=18,
    height=2,
    command=stop_monitoring
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Register Resident",
    width=18,
    height=2,
    command=register_resident
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="View Logs",
    width=18,
    height=2,
    command=view_logs
).grid(row=1, column=0, padx=5, pady=10)

tk.Button(
    button_frame,
    text="View Screenshots",
    width=18,
    height=2,
    command=view_screenshots
).grid(row=1, column=1, padx=5, pady=10)

tk.Button(
    button_frame,
    text="Exit",
    width=18,
    height=2,
    command=exit_app
).grid(row=1, column=2, padx=5, pady=10)

root.mainloop()