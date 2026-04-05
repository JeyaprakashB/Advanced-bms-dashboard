import customtkinter as ctk
import random

# ---------------- THEME ---------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ---------------- FUNCTIONS ---------------- #

def calculate_soc(voltage):
    v_max = 4.2
    v_min = 3.0
    soc = ((voltage - v_min) / (v_max - v_min)) * 100
    return max(0, min(100, round(soc, 2)))

def battery_status(current):
    if current > 0:
        return "Charging"
    elif current < 0:
        return "Discharging"
    else:
        return "Idle"

def temperature_status(temp):
    if temp < 25:
        return "Cool"
    elif temp <= 45:
        return "Normal"
    elif temp <= 60:
        return "High"
    else:
        return "Overheating ⚠"

def safety_check(temp, current):
    if temp > 60:
        return "⚠ Critical: Overheating"
    elif current > 5:
        return "⚠ Overcurrent Risk"
    else:
        return "Safe"

# ---------------- MAIN FUNCTION ---------------- #

def check_battery():
    try:
        v = float(voltage_entry.get())
        i = float(current_entry.get())
        t = float(temp_entry.get())

        soc = calculate_soc(v)
        status = battery_status(i)
        temp_stat = temperature_status(t)
        safety = safety_check(t, i)

        # Update UI
        soc_label.configure(text=f"SOC: {soc}%")
        status_label.configure(text=f"Status: {status}")
        temp_label.configure(text=f"Temperature: {temp_stat}")
        safety_label.configure(text=f"Safety: {safety}")

        progress.set(soc / 100)

        # Temperature color
        if t < 45:
            temp_label.configure(text_color="#22c55e")  # green
        elif t < 60:
            temp_label.configure(text_color="#facc15")  # yellow
        else:
            temp_label.configure(text_color="#ef4444")  # red

        # Safety color
        if "Safe" in safety:
            safety_label.configure(text_color="#22c55e")
        else:
            safety_label.configure(text_color="#ef4444")

    except:
        safety_label.configure(text="Invalid Input", text_color="orange")

# ---------------- AUTO INPUT ---------------- #

def auto_input():
    v = round(random.uniform(3.0, 4.2), 2)
    i = round(random.uniform(-5, 6), 2)
    t = random.randint(20, 70)

    voltage_entry.delete(0, "end")
    current_entry.delete(0, "end")
    temp_entry.delete(0, "end")

    voltage_entry.insert(0, str(v))
    current_entry.insert(0, str(i))
    temp_entry.insert(0, str(t))

# ---------------- UI ---------------- #

app = ctk.CTk()
app.title("🔋 Advanced BMS Dashboard")
app.geometry("460x560")

# 🔥 Liquid-style background
app.configure(fg_color="#0f172a")

# Background layer (depth effect)
bg_frame = ctk.CTkFrame(app, fg_color="#020617", corner_radius=0)
bg_frame.place(relwidth=1, relheight=1)

# Title
title = ctk.CTkLabel(
    app,
    text="⚡ Battery Management System",
    font=("Arial", 22, "bold"),
    text_color="#e2e8f0"
)
title.pack(pady=15)

# -------- INPUT CARD -------- #
input_frame = ctk.CTkFrame(
    app,
    corner_radius=20,
    fg_color="#1e293b",
    border_width=2,
    border_color="#38bdf8"
)
input_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(
    input_frame,
    text="Input Parameters",
    font=("Arial", 16, "bold"),
    text_color="#e2e8f0"
).pack(pady=10)

voltage_entry = ctk.CTkEntry(input_frame, placeholder_text="Voltage (3.0V - 4.2V)")
voltage_entry.pack(pady=8)

current_entry = ctk.CTkEntry(input_frame, placeholder_text="Current (-5 to +5 A)")
current_entry.pack(pady=8)

temp_entry = ctk.CTkEntry(input_frame, placeholder_text="Temperature (°C)")
temp_entry.pack(pady=8)

ctk.CTkButton(
    input_frame,
    text="Check Battery",
    command=check_battery,
    fg_color="#38bdf8",
    hover_color="#0ea5e9",
    corner_radius=12
).pack(pady=10)

ctk.CTkButton(
    input_frame,
    text="Auto Input",
    command=auto_input,
    fg_color="#6366f1",
    hover_color="#4f46e5",
    corner_radius=12
).pack(pady=5)

# -------- OUTPUT CARD -------- #
output_frame = ctk.CTkFrame(
    app,
    corner_radius=20,
    fg_color="#1e293b",
    border_width=2,
    border_color="#38bdf8"
)
output_frame.pack(pady=15, padx=20, fill="x")

ctk.CTkLabel(
    output_frame,
    text="Battery Status",
    font=("Arial", 16, "bold"),
    text_color="#e2e8f0"
).pack(pady=10)

# Progress bar (battery)
progress = ctk.CTkProgressBar(output_frame, width=250)
progress.pack(pady=10)
progress.set(0)

# Labels
soc_label = ctk.CTkLabel(output_frame, text="SOC: ---", font=("Arial", 14))
soc_label.pack(pady=5)

status_label = ctk.CTkLabel(output_frame, text="Status: ---", font=("Arial", 14))
status_label.pack(pady=5)

temp_label = ctk.CTkLabel(output_frame, text="Temperature: ---", font=("Arial", 14))
temp_label.pack(pady=5)

safety_label = ctk.CTkLabel(output_frame, text="Safety: ---", font=("Arial", 14, "bold"))
safety_label.pack(pady=10)

# Run app
app.mainloop()