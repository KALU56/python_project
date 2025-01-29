import uuid
import re
import register  # Importing register.py
from datetime import datetime

def validate_email(email):
    """Check if the email is in a valid format."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
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

def appointment():
    email = input("Enter your email address: ").strip()

    if not validate_email(email):
        print("Invalid email format. Please enter a valid email address.")
        return

    donor_id = find_donor_by_email(email)
    if not donor_id:
        print("No donor found with this email. Please register first.")
        register.register()  # Call register if donor is not found
        donor_id = find_donor_by_email(email)  # Try fetching donor ID again
        if not donor_id:
            print("Registration failed. Cannot proceed with appointment.")
            return

    appointment_id = str(uuid.uuid4())
    supervisor_id = str(uuid.uuid4())

    while True:
        appointment_date = input("Enter your appointment date (YYYY-MM-DD): ").strip()
        if validate_date(appointment_date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    while True:
        appointment_time = input("Enter your appointment time (HH:MM): ").strip()
        if validate_time(appointment_time):
            break
        print("Invalid time format. Please use HH:MM.")

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

        print("Your appointment has been scheduled successfully!")

    except Exception as e:
        print(f"Error saving appointment: {e}")

