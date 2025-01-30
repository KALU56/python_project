import tkinter as tk
from tkinter import messagebox
import GUI.register_gui as register_gui  # Ensure this file exists and is in the same directory
import GUI.appointment_gui as appointment_gui  # Ensure this file exists and contains the appointment() function

def register_donor():
    register_gui.register_donor()  # Open donor registration window

def schedule_appointment():
    appointment_gui.appointment()  # Open appointment scheduling window

def view_medical_info():
    messagebox.showinfo("Medical Information", "This feature is under development.")

def exit_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Donor Bank X")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Create a label for the title
title_label = tk.Label(root, text="Welcome to Donor Bank X!", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Create buttons
register_button = tk.Button(root, text="Register a New Donor", command=register_donor, width=30, height=2, bg="#4CAF50", fg="white")
register_button.pack(pady=5)

appointment_button = tk.Button(root, text="Schedule an Appointment", command=schedule_appointment, width=30, height=2, bg="#2196F3", fg="white")
appointment_button.pack(pady=5)

medical_button = tk.Button(root, text="View Medical Information", command=view_medical_info, width=30, height=2, bg="#FF9800", fg="white")
medical_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_app, width=30, height=2, bg="#f44336", fg="white")
exit_button.pack(pady=5)

# Run the main loop
root.mainloop()
