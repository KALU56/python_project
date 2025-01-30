import tkinter as tk
from tkinter import messagebox
import uuid
import re
from datetime import datetime
import register_gui  # Ensure this file exists and contains the register function
from +donor_gui import find_donor_by_email

  # Ensure this file exists and contains the find_donor_by_email function

# Validation Functions
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

# Find donor by email (from donor_gui.py)
def find_donor_by_email(email):
    """Search donor_registration.txt for a donor by email and return DonorID."""
    try:
        with open("donor_registration.txt", "r") as file:
            donor_id = None
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("Email:") and lines[i].strip().split()[1] == email:
                    # Extract DonorID
                    for j in range(max(0, i - 10), i):
                        if lines[j].startswith("DonorID:"):
                            donor_id = lines[j].strip().split()[1]
                            return donor_id
        return None
    except FileNotFoundError:
        print("Error: Donor registration file not found.")
        return None

# Schedule Appointment Function
def schedule_appointment():
    """Function to open the appointment scheduling window."""
    def submit_appointment():
        email = email_entry.get().strip()

        # Validate email format
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return

        donor_id = find_donor_by_email(email)
        if not donor_id:
            messagebox.showinfo("Info", "No donor found with this email. Please register first.")
            register_gui.register_donor()  # Call register if donor is not found
            donor_id = find_donor_by_email(email)  # Try fetching donor ID again
            if not donor_id:
                messagebox.showerror("Error", "Registration failed. Cannot proceed with appointment.")
                return

        appointment_id = str(uuid.uuid4())
        supervisor_id = str(uuid.uuid4())

        # Validate appointment date
        appointment_date = appointment_date_entry.get().strip()
        if not validate_date(appointment_date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Validate appointment time
        appointment_time = appointment_time_entry.get().strip()
        if not validate_time(appointment_time):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
            return

        appointment_status = "Scheduled"

        # Save appointment details to the appointments.txt file
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

    # Create a new window for appointment scheduling
    appointment_window = tk.Toplevel()
    appointment_window.title("Schedule Appointment")
    appointment_window.geometry("400x300")

    # Labels and Entry fields for appointment details
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

# Create a function to open the appointment scheduling window when needed
def appointment():
    schedule_appointment()
