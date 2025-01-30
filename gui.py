import tkinter as tk
from tkinter import messagebox
import uuid
import re
from datetime import datetime

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
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# GUI Application
class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank System")
        
        # Create frames for different sections
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.frame, text="Welcome to Blood Bank System", font=("Arial", 16))
        title.grid(row=0, columnspan=2, pady=10)

        # Donor Registration
        tk.Label(self.frame, text="First Name:").grid(row=1, column=0, sticky=tk.W)
        self.first_name_entry = tk.Entry(self.frame)
        self.first_name_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Last Name:").grid(row=2, column=0, sticky=tk.W)
        self.last_name_entry = tk.Entry(self.frame)
        self.last_name_entry.grid(row=2, column=1)

        tk.Label(self.frame, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W)
        self.dob_entry = tk.Entry(self.frame)
        self.dob_entry.grid(row=3, column=1)

        tk.Label(self.frame, text="Gender (Male/Female):").grid(row=4, column=0, sticky=tk.W)
        self.gender_entry = tk.Entry(self.frame)
        self.gender_entry.grid(row=4, column=1)

        tk.Label(self.frame, text="Blood Type:").grid(row=5, column=0, sticky=tk.W)
        self.blood_type_entry = tk.Entry(self.frame)
        self.blood_type_entry.grid(row=5, column=1)

        tk.Label(self.frame, text="Email:").grid(row=6, column=0, sticky=tk.W)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=6, column=1)

        tk.Label(self.frame, text="Phone Number:").grid(row=7, column=0, sticky=tk.W)
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.grid(row=7, column=1)

        # Register Button
        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=8, columnspan=2, pady=10)

        # Appointment Section
        tk.Label(self.frame, text="Appointment Date (YYYY-MM-DD):").grid(row=9, column=0, sticky=tk.W)
        self.appointment_date_entry = tk.Entry(self.frame)
        self.appointment_date_entry.grid(row=9, column=1)

        tk.Label(self.frame, text="Appointment Time (HH:MM):").grid(row=10, column=0, sticky=tk.W)
        self.appointment_time_entry = tk.Entry(self.frame)
        self.appointment_time_entry.grid(row=10, column=1)
              # Schedule Appointment Button
        self.schedule_button = tk.Button(self.frame, text="Schedule Appointment", command=self.schedule_appointment)
        self.schedule_button.grid(row=11, columnspan=2, pady=10)

        # View Medical History Button
        self.view_medical_button = tk.Button(self.frame, text="View Medical History", command=self.view_medical_history)
        self.view_medical_button.grid(row=12, columnspan=2, pady=10)

    def register(self):
        # Collect donor information
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        gender = self.gender_entry.get().strip().capitalize()
        blood_type = self.blood_type_entry.get().strip().upper()
        email = self.email_entry.get().strip()
        phone_number = self.phone_entry.get().strip()

        # Validate inputs
        if not all([first_name, last_name, dob, gender, blood_type, email, phone_number]):
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        if not validate_date_of_birth(dob):
            messagebox.showerror("Input Error", "You must be 18 or older.")
            return

        if not validate_email(email):
            messagebox.showerror("Input Error", "Invalid email format.")
            return

        if not validate_phone_number(phone_number):
            messagebox.showerror("Input Error", "Invalid phone number format.")
            return

        # Generate a unique DonorID
        donor_id = str(uuid.uuid4())

        # Save donor information to file
        with open("donor_registration.txt", "a") as file:
            file.write(f"DonorID: {donor_id}\n")
            file.write(f"FirstName: {first_name}\n")
            file.write(f"LastName: {last_name}\n")
            file.write(f"DateOfBirth: {dob}\n")
            file.write(f"Gender: {gender}\n")
            file.write(f"BloodType: {blood_type}\n")
            file.write(f"Email: {email}\n")
            file.write(f"PhoneNumber: {phone_number}\n")
            file.write("----------------------------------------\n")

        messagebox.showinfo("Success", "Registration successful!")

    def schedule_appointment(self):
        # Collect appointment information
        appointment_date = self.appointment_date_entry.get().strip()
        appointment_time = self.appointment_time_entry.get().strip()

        # Validate inputs
        if not validate_date(appointment_date):
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        if not validate_time(appointment_time):
            messagebox.showerror("Input Error", "Invalid time format. Use HH:MM.")
            return

        # Find donor by email (for simplicity, we will ask for email again)
        email = self.email_entry.get().strip()
        donor_id = self.find_donor_by_email(email)

        if not donor_id:
            messagebox.showerror("Error", "No donor found with this email. Please register first.")
            return

        # Generate a unique AppointmentID
        appointment_id = str(uuid.uuid4())
        supervisor_id = str(uuid.uuid4())  # Placeholder for supervisor ID

        # Save appointment information to file
        with open("appointments.txt", "a") as appt_file:
            appt_file.write(f"AppointmentID: {appointment_id}\n")
            appt_file.write(f"DonorID: {donor_id}\n")
            appt_file.write(f"SupervisorID: {supervisor_id}\n")
            appt_file.write(f"AppointmentDate: {appointment_date}\n")
            appt_file.write(f"AppointmentTime: {appointment_time}\n")
            appt_file.write(f"AppointmentStatus: Scheduled\n")
            appt_file.write("----------------------------------------\n")

        messagebox.showinfo("Success", "Appointment scheduled successfully!")

    def find_donor_by_email(self, email):
        """Search donor_registration.txt for a donor by email and return DonorID."""
        try:
            with open("donor_registration.txt", "r") as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    if lines[i].startswith("Email:") and lines[i].strip().split()[1] == email:
                        # Extract DonorID
                        for j in range(max(0, i - 10), i):
                            if lines[j].startswith("DonorID:"):
                                return lines[j].strip().split()[1]
            return None
        except FileNotFoundError:
                        messagebox.showerror("Error", "Donor registration file not found.")
            

    def view_medical_history(self):
        email = self.email_entry.get().strip()
        donor_id = self.find_donor_by_email(email)

        if not donor_id:
            messagebox.showerror("Error", "No donor found with this email.")
            return

        try:
            with open("medical_history.txt", "r") as med_file:
                medical_records = []
                current_record = {}
                for line in med_file:
                    line = line.strip()
                    if line.startswith("HistoryID:"):
                        if current_record:  # Save the previous record
                            medical_records.append(current_record)
                        current_record = {"HistoryID": line.split(":")[1].strip()}
                    elif line.startswith("DonorID:") and line.split(":")[1].strip() == donor_id:
                        current_record["DonorID"] = line.split(":")[1].strip()
                    elif line.startswith("HIV:"):
                        current_record["HIV"] = line.split(":")[1].strip()
                    elif line.startswith("Syphilis:"):
                        current_record["Syphilis"] = line.split(":")[1].strip()
                    elif line.startswith("Hepatitis_B:"):
                        current_record["Hepatitis_B"] = line.split(":")[1].strip()
                    elif line.startswith("Hepatitis_C:"):
                        current_record["Hepatitis_C"] = line.split(":")[1].strip()
                    elif line.startswith("SugarLevel:"):
                        current_record["SugarLevel"] = line.split(":")[1].strip()
                    elif line.startswith("OutcomeDetails:"):
                        current_record["OutcomeDetails"] = line.split(":")[1].strip()

                if current_record:  # Add the last one if any
                    medical_records.append(current_record)

            if medical_records:
                history_info = "\nYour Medical History:\n"
                for record in medical_records:
                    history_info += (f"History ID: {record['HistoryID']}\n"
                                     f"  HIV: {record['HIV']}\n"
                                     f"  Syphilis: {record['Syphilis']}\n"
                                     f"  Hepatitis B: {record['Hepatitis_B']}\n"
                                     f"  Hepatitis C: {record['Hepatitis_C']}\n"
                                     f"  Sugar Level: {record['SugarLevel']}\n"
                                     f"  Outcome Details: {record['OutcomeDetails']}\n"
                                     "----------------------------------------\n")
                messagebox.showinfo("Medical History", history_info)
            else:
                messagebox.showinfo("Medical History", "No medical history found for you.")

        except FileNotFoundError:
            messagebox.showerror("Error", "Medical history file not found.")

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BloodBankApp(root)
    root.mainloop()