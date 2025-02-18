import tkinter as tk
from tkinter import messagebox, scrolledtext
import uuid
import re
from datetime import datetime

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
        DonorPortal(donor_window)

    def go_to_supervisor(self):
        supervisor_window = tk.Toplevel(self.root)
        SupervisorPortal(supervisor_window)

class DonorPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Activity")
        self.root.geometry("400x300")
        
        donor_label = tk.Label(self.root, text="Welcome to the Donor Activity", font=("Helvetica", 14))
        donor_label.pack(pady=20)

        registration_button = tk.Button(self.root, text="Registration", font=("Helvetica", 12), 
                                      command=self.open_registration)
        registration_button.pack(pady=10)

        login_button = tk.Button(self.root, text="Login", font=("Helvetica", 12), 
                               command=self.open_login)
        login_button.pack(pady=10)

        exit_button = tk.Button(self.root, text="Exit", font=("Helvetica", 12), command=self.root.destroy)
        exit_button.pack(pady=10)

    def open_registration(self):
        registration_window = tk.Toplevel(self.root)
        DonorRegistrationForm(registration_window)

    def open_login(self):
        login_window = tk.Toplevel(self.root)
        DonorLoginForm(login_window)

class SupervisorPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Supervisor Portal")
        self.root.geometry("400x300")

        login_button = tk.Button(self.root, text="Login", font=("Helvetica", 12), 
                               command=self.open_login)
        login_button.pack(pady=50)

        exit_button = tk.Button(self.root, text="Exit", font=("Helvetica", 12), command=self.root.destroy)
        exit_button.pack(pady=10)

    def open_login(self):
        login_window = tk.Toplevel(self.root)
        SupervisorLoginForm(login_window, self.root)

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
       # Login logic remains the same as original
        # ... (Include donor login logic here)

class SupervisorLoginForm:
    def __init__(self, root, parent_window):
        self.root = root
        self.parent_window = parent_window
        self.root.title("Supervisor Login")
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

        if username == "sup" and password == "1234":
            self.root.destroy()
            self.parent_window.destroy()
            self.open_supervisor_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def open_supervisor_dashboard(self):
        dashboard = tk.Toplevel()
        dashboard.title("Supervisor Dashboard")
        dashboard.geometry("400x300")

        see_donors_button = tk.Button(dashboard, text="View All Donors", 
                                    command=self.show_all_donors)
        see_donors_button.pack(pady=20)
        send_medical_history_button = tk.Button(dashboard, text="medical_history", 
                                    command=self.send_medical_history)
        send_medical_history_button.pack(pady=20)
        exit_button = tk.Button(dashboard, text="Exit", 
                              command=dashboard.destroy)
        exit_button.pack(pady=10)

    def show_all_donors(self):
        try:
            with open("donor_registration.txt", "r") as f:
                donors_data = f.read()
                if not donors_data.strip():
                    messagebox.showinfo("Donors", "No donors registered yet")
                    return

                donors_window = tk.Toplevel()
                donors_window.title("Registered Donors")
                text_area = scrolledtext.ScrolledText(donors_window, wrap=tk.WORD)
                text_area.pack(expand=True, fill="both")
                text_area.insert(tk.INSERT, donors_data)
                text_area.configure(state='disabled')
        except FileNotFoundError:
            messagebox.showerror("Error", "Donor records not found")
   
class MedicalHistoryForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Record Medical History")
        self.root.geometry("500x600")

        tk.Label(self.root, text="Donor Email or Username:").pack(pady=5)
        self.donor_identifier_entry = tk.Entry(self.root)
        self.donor_identifier_entry.pack(pady=5)

        conditions = ["HIV", "Syphilis", "Hepatitis B", "Hepatitis C"]
        self.condition_vars = {}
        for condition in conditions:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{condition}:").pack(side=tk.LEFT)
            var = tk.StringVar(value="0")
            self.condition_vars[condition] = var
            tk.Radiobutton(frame, text="Yes", variable=var, value="1").pack(side=tk.LEFT)
            tk.Radiobutton(frame, text="No", variable=var, value="0").pack(side=tk.LEFT)

        tk.Label(self.root, text="Sugar Level:").pack(pady=5)
        self.sugar_entry = tk.Entry(self.root)
        self.sugar_entry.pack(pady=5)

        tk.Label(self.root, text="Outcome Details:").pack(pady=5)
        self.outcome_entry = tk.Entry(self.root)
        self.outcome_entry.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def check_donor_exists(self, identifier):
        try:
            with open("donor_registration.txt", "r") as f:
                content = f.read()
                blocks = content.split('-'*40 + '\n')
                for block in blocks:
                    if not block.strip():
                        continue
                    lines = block.split('\n')
                    donor_data = {}
                    for line in lines:
                        if line.strip():
                            key, val = line.split(': ', 1)
                            donor_data[key.strip()] = val.strip()
                    if donor_data.get('username') == identifier or donor_data.get('email') == identifier:
                        return donor_data.get('username')  # Return username
                return None
        except FileNotFoundError:
            return None

    def submit(self):
        identifier = self.donor_identifier_entry.get().strip()
        if not identifier:
            messagebox.showerror("Error", "Please enter donor email or username.")
            return

        donor_username = self.check_donor_exists(identifier)
        if not donor_username:
            messagebox.showerror("Error", "Donor not registered.")
            return

        hiv = self.condition_vars["HIV"].get()
        syphilis = self.condition_vars["Syphilis"].get()
        hepatitis_b = self.condition_vars["Hepatitis B"].get()
        hepatitis_c = self.condition_vars["Hepatitis C"].get()
        sugar_level = self.sugar_entry.get().strip()
        outcome_details = self.outcome_entry.get().strip()

        if not sugar_level:
            messagebox.showerror("Error", "Sugar Level is required.")
            return

        history_id = str(uuid.uuid4())
        try:
            with open("medical_history.txt", "a") as file:
                file.write(f"HistoryID: {history_id}\n")
                file.write(f"Username: {donor_username}\n")
                file.write(f"HIV: {hiv}\n")
                file.write(f



# Include DonorAppointmentForm class here if needed

if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomePage(root)
    root.mainloop()