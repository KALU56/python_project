import tkinter as tk
from tkinter import messagebox
import uuid
import re
from datetime import datetime
from datetime import datetime, timedelta
class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome Page")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Welcome to the Blood Bank Management System", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.donor_button = tk.Button(root, text="Donor", font=("Helvetica", 12), command=self.go_to_donor)
        self.donor_button.pack(pady=10)

        self.supervisor_button = tk.Button(root, text="Supervisor", font=("Helvetica", 12), command=self.go_to_supervisor)
        self.supervisor_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=self.root.quit)
        self.exit_button.pack(pady=10)

    def go_to_donor(self):
        donor_window = tk.Toplevel(self.root)
        donor_window.title("Donor Activity")
        donor_window.geometry("400x300")
        donor_label = tk.Label(donor_window, text="Welcome to the Donor Activity", font=("Helvetica", 14))
        donor_label.pack(pady=20)

        registration_button = tk.Button(donor_window, text="Registration", font=("Helvetica", 12), 
                                        command=lambda: DonorRegistrationForm(tk.Toplevel(donor_window)))
        registration_button.pack(pady=10)

        login_button = tk.Button(donor_window, text="Login", font=("Helvetica", 12), 
                                 command=lambda: DonorLoginForm(tk.Toplevel(donor_window)))
        login_button.pack(pady=10)

        donor_exit_button = tk.Button(donor_window, text="Exit", font=("Helvetica", 12), command=donor_window.destroy)
        donor_exit_button.pack(pady=10)

    def go_to_supervisor(self):
        supervisor_window = tk.Toplevel(self.root)
        supervisor_window.title("Supervisor Dashboard")
        supervisor_window.geometry("400x300")
        supervisor_label = tk.Label(supervisor_window, text="Welcome to the Supervisor Dashboard", font=("Helvetica", 14))
        supervisor_label.pack(pady=20)

        supervisor_exit_button = tk.Button(supervisor_window, text="Exit", font=("Helvetica", 12), command=supervisor_window.destroy)
        supervisor_exit_button.pack(pady=10)

class DonorRegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Registration")
        self.root.geometry("400x600")

        self.donor_id = str(uuid.uuid4())

        fields = [
            ("Username:", "username_entry"),
            ("Password:", "password_entry"),
            ("First Name:", "first_name_entry"),
            ("Last Name:", "last_name_entry"),
            ("Date of Birth (YYYY-MM-DD):", "dob_entry"),
            ("Gender (Male/Female):", "gender_entry"),
            ("Blood Type (A, B, O, A+, A-, O+, O-, B+, B-):", "blood_type_entry"),
            ("Email (optional, must be Gmail if provided):", "email_entry"),
            ("Phone Number (09 or 07):", "phone_number_entry")
        ]

        for text, _ in fields:
            label = tk.Label(self.root, text=text)
            label.pack()
            entry = tk.Entry(self.root)
            entry.pack()
            setattr(self, _, entry)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.register)
        self.submit_button.pack(pady=20)

    def validate_date_of_birth(self, dob):
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.today() - birth_date).days // 365
            return age >= 18
        except ValueError:
            return False

    def validate_phone_number(self, phone_number):
        return re.match(r"^(09|07)\d{8}$", phone_number) is not None

    def validate_email(self, email):
        if email == "":
            return True
        return re.match(r"^[a-zA-Z0-9_.+-]+@gmail\.com$", email) is not None

    def validate_blood_type(self, blood_type):
        if blood_type == "":
            return True
        valid_blood_types = ["A", "B", "O", "A+", "A-", "O+", "O-", "B+", "B-"]
        return blood_type in valid_blood_types

    def register(self):
        data = {
            "username": self.username_entry.get().strip(),
            "password": self.password_entry.get().strip(),
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "dob": self.dob_entry.get(),
            "gender": self.gender_entry.get().strip().capitalize(),
            "blood_type": self.blood_type_entry.get().strip().upper(),
            "email": self.email_entry.get().strip(),
            "phone_number": self.phone_number_entry.get().strip()
        }

        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not self.validate_date_of_birth(data["dob"]):
            messagebox.showerror("Error", "Invalid date or age < 18. Use YYYY-MM-DD.")
            return

        if not self.validate_phone_number(data["phone_number"]):
            messagebox.showerror("Error", "Invalid phone number. Must start with 09/07 and 10 digits.")
            return

        if not self.validate_email(data["email"]):
            messagebox.showerror("Error", "Invalid email. Only Gmail addresses accepted.")
            return

        if not self.validate_blood_type(data["blood_type"]):
            messagebox.showerror("Error", "Invalid blood type. Must be one of A, B, O, A+, A-, O+, O-, B+, B-.")
            return

        with open("donor_registration.txt", "a") as f:
            f.write(f"DonorID: {self.donor_id}\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
            f.write("-" * 40 + "\n")

        messagebox.showinfo("Success", "Registration successful!")
        self.root.destroy()

class DonorLoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Login")
        self.root.geometry("400x300")

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        with open("donor_registration.txt", "r") as f:
            data = f.read()
            if username in data and password in data:
                donor_activity_window = tk.Toplevel(self.root)
                donor_activity_window.title("Donor Activity")
                donor_activity_window.geometry("400x400")

                appointment_button = tk.Button(donor_activity_window, text="Appointment", font=("Helvetica", 12), 
                                                command=lambda: Donorappointmentform(tk.Toplevel(donor_activity_window)))
                appointment_button.pack(pady=10)

                medical_history_button = tk.Button(donor_activity_window, text="Medical History", font=("Helvetica", 12), 
                                                   command=self.go_to_medical_history)
                medical_history_button.pack(pady=10)

                medical_status_button = tk.Button(donor_activity_window, text="Medical Status", font=("Helvetica", 12), 
                                                  command=self.go_to_medical_status)
                medical_status_button.pack(pady=10)

                donor_exit_button = tk.Button(donor_activity_window, text="Exit", font=("Helvetica", 12), command=donor_activity_window.destroy)
                donor_exit_button.pack(pady=10)

            else:
                messagebox.showerror("Error", "Invalid username or password.")

    def go_to_medical_history(self):
        messagebox.showinfo("Medical History", "Medical History functionality not implemented yet.")

    def go_to_medical_status(self):
        messagebox.showinfo("Medical Status", "Medical Status functionality not implemented yet.")
class Donorappointmentform:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Form")
        self.root.geometry("400x400")

        self.appointment_time_label = tk.Label(self.root, text="Select Appointment Date and Time:")
        self.appointment_time_label.pack(pady=10)

        self.appointment_date_entry = tk.Entry(self.root)
        self.appointment_date_entry.pack(pady=5)
        self.appointment_date_entry.insert(0, self.get_current_date())  # Set default to current date

        self.appointment_time_label = tk.Label(self.root, text="Select Appointment Time (HH:MM):")
        self.appointment_time_label.pack(pady=10)

        self.appointment_time_entry = tk.Entry(self.root)
        self.appointment_time_entry.pack(pady=5)
        self.appointment_time_entry.insert(0, "12:00")  # Default time

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_appointment)
        self.submit_button.pack(pady=20)

    def get_current_date(self):
        return datetime.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format

    def validate_appointment(self, appointment_date, appointment_time):
        # Get the current date and time
        now = datetime.now()
        # Parse the appointment date and time entered by the user
        try:
            appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return False, "Invalid date or time format. Please use YYYY-MM-DD for the date and HH:MM for the time."
        
        # Check if the appointment date and time is in the past
        if appointment_datetime < now:
            return False, "Appointment time cannot be in the past."
        return True, ""

    def submit_appointment(self):
        appointment_date = self.appointment_date_entry.get().strip()
        appointment_time = self.appointment_time_entry.get().strip()

        # Validate if the date and time are in the correct format and not in the past
        valid, message = self.validate_appointment(appointment_date, appointment_time)
        if not valid:
            messagebox.showerror("Error", message)
            return

        # If valid, save the appointment (you could save it to a file or database)
        with open("appointments.txt", "a") as f:
            f.write(f"Appointment Date: {appointment_date} Time: {appointment_time}\n")

        messagebox.showinfo("Success", "Appointment scheduled successfully!")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomePage(root)
    root.mainloop()
