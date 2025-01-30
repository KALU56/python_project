import tkinter as tk
from tkinter import messagebox
import uuid
from datetime import datetime
import re
import  register_gui  # Ensure this file contains the necessary function
# import appointment_gui  # Ensure this file contains the necessary function

# Validation functions
def validate_date_of_birth(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.today() - birth_date).days // 365
        return age >= 18
    except ValueError:
        return False

def validate_phone_number(phone_number):
    return re.match(r"^(09|07)\d{8}$", phone_number) is not None

def validate_email(email):
    """Check if the email is in a valid format."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zAZ0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """Validate time format (HH:MM)."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Find donor by email
def find_donor_by_email(email):
    """Search for a donor by email."""
    try:
        with open("donor_registration.txt", "r") as file:
            donor_id = None
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("Email:") and lines[i].strip().split()[1] == email:
                    for j in range(max(0, i - 10), i):
                        if lines[j].startswith("DonorID:"):
                            donor_id = lines[j].strip().split()[1]
                            return donor_id
        return None
    except FileNotFoundError:
        print("Error: Donor registration file not found.")
        return None

# Schedule appointment function
def schedule_appointment():
    def submit_appointment():
        email = email_entry.get().strip()

        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return

        donor_id = find_donor_by_email(email)
        if not donor_id:
            messagebox.showinfo("Info", "No donor found with this email. Please register first.")
            register_gui.register()  # Trigger donor registration
            donor_id = find_donor_by_email(email)  # Retry fetching donor ID
            if not donor_id:
                messagebox.showerror("Error", "Registration failed. Cannot proceed with appointment.")
                return

        appointment_id = str(uuid.uuid4())
        supervisor_id = str(uuid.uuid4())

        # Validate date and time
        appointment_date = appointment_date_entry.get().strip()
        if not validate_date(appointment_date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        appointment_time = appointment_time_entry.get().strip()
        if not validate_time(appointment_time):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
            return

        appointment_status = "Scheduled"

        try:
            with open("appointments.txt", "a") as appt_file:
                appt_file.write(f"AppointmentID: {appointment_id}\n")
                appt_file.write(f"DonorID: {donor_id}\n")
                appt_file.write(f"SupervisorID: {supervisor_id}\n")
                appt_file.write(f"AppointmentDate: {appointment_date}\n")
                appt_file.write(f"AppointmentTime: {appointment_time}\n")
                appt_file.write(f"AppointmentStatus: {appointment_status}\n")
                appt_file.write("----------------------------------------\n")

            messagebox.showinfo("Success", "Your appointment has been scheduled successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving appointment: {e}")

    # Create appointment window
    appointment_window = tk.Toplevel()
    appointment_window.title("Schedule Appointment")
    appointment_window.geometry("400x300")

    tk.Label(appointment_window, text="Enter your email address:").pack()
    email_entry = tk.Entry(appointment_window)
    email_entry.pack()

    tk.Label(appointment_window, text="Enter appointment date (YYYY-MM-DD):").pack()
    appointment_date_entry = tk.Entry(appointment_window)
    appointment_date_entry.pack()

    tk.Label(appointment_window, text="Enter appointment time (HH:MM):").pack()
    appointment_time_entry = tk.Entry(appointment_window)
    appointment_time_entry.pack()

    tk.Button(appointment_window, text="Schedule Appointment", command=submit_appointment).pack()

# Register donor function
def register_donor():
    register_gui.register_donor()  # Call donor registration window from register_gui

# View medical info (under development placeholder)
def view_medical_info():
    messagebox.showinfo("Medical Information", "This feature is under development.")

# Exit application
def exit_app():
    root.quit()

# Main window setup
root = tk.Tk()
root.title("Donor Bank X")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Create title label
title_label = tk.Label(root, text="Welcome to Donor Bank X!", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Create navigation buttons
register_button = tk.Button(root, text="Register a New Donor", command=register_donor, width=30, height=2, bg="#4CAF50", fg="white")
register_button.pack(pady=5)

appointment_button = tk.Button(root, text="Schedule an Appointment", command=schedule_appointment, width=30, height=2, bg="#2196F3", fg="white")
appointment_button.pack(pady=5)

medical_button = tk.Button(root, text="View Medical Information", command=view_medical_info, width=30, height=2, bg="#FF9800", fg="white")
medical_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_app, width=30, height=2, bg="#f44336", fg="white")
exit_button.pack(pady=5)

# Start main event loop
root.mainloop()
