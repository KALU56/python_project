import tkinter as tk
from tkinter import messagebox
import pyodbc
import re
from datetime import datetime

# Database Connection
class DBConfig:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=KALKIDAN;"
                "DATABASE=BloodBankDB;"
                "UID=sa;PWD=kalkidan"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except Exception as e:
            messagebox.showerror("Query Error", f"Failed to execute query: {e}")

# Donor Registration Form
class DonorRegistrationForm:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Donor Registration")
        
        tk.Label(root, text="Full Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Age:").grid(row=1, column=0)
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Phone Number:").grid(row=2, column=0)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Blood Type:").grid(row=3, column=0)
        self.blood_type_entry = tk.Entry(root)
        self.blood_type_entry.grid(row=3, column=1)
        
        tk.Button(root, text="Register", command=self.register_donor).grid(row=4, columnspan=2)
    
    def register_donor(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        phone = self.phone_entry.get()
        blood_type = self.blood_type_entry.get()
        
        if not re.match(r"^(\+2519|09)\d{8}$", phone):
            messagebox.showerror("Validation Error", "Invalid phone number format.")
            return
        
        try:
            query = """
            INSERT INTO Donors (FullName, Age, PhoneNumber, BloodType)
            VALUES (?, ?, ?, ?)
            """
            self.db.execute_query(query, (name, age, phone, blood_type))
            messagebox.showinfo("Success", "Donor registered successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

# Appointment Scheduler
class AppointmentScheduler:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Schedule Appointment")
        
        tk.Label(root, text="Donor ID:").grid(row=0, column=0)
        self.donor_id_entry = tk.Entry(root)
        self.donor_id_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=1, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Time (HH:MM):").grid(row=2, column=0)
        self.time_entry = tk.Entry(root)
        self.time_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Notes:").grid(row=3, column=0)
        self.notes_entry = tk.Entry(root)
        self.notes_entry.grid(row=3, column=1)
        
        tk.Button(root, text="Schedule", command=self.schedule_appointment).grid(row=4, columnspan=2)
    
    def schedule_appointment(self):
        donor_id = self.donor_id_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        notes = self.notes_entry.get()
        
        try:
            appointment_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            query = """
            INSERT INTO Appointments (DonorID, AppointmentDateTime, Status, Message)
            VALUES (?, ?, ?, ?)
            """
            self.db.execute_query(query, (donor_id, appointment_time, 'Pending', notes))
            messagebox.showinfo("Success", "Appointment scheduled successfully!")
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid date or time format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")

# Supervisor Management
class SupervisorDashboard:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Supervisor Panel")
        
        tk.Label(root, text="Appointment ID:").grid(row=0, column=0)
        self.appointment_id_entry = tk.Entry(root)
        self.appointment_id_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Status (Approved/Rejected):").grid(row=1, column=0)
        self.status_entry = tk.Entry(root)
        self.status_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Message:").grid(row=2, column=0)
        self.message_entry = tk.Entry(root)
        self.message_entry.grid(row=2, column=1)
        
        tk.Button(root, text="Update Status", command=self.update_status).grid(row=3, columnspan=2)
    
    def update_status(self):
        appointment_id = self.appointment_id_entry.get()
        status = self.status_entry.get()
        message = self.message_entry.get()
        
        if status not in ['Approved', 'Rejected']:
            messagebox.showerror("Validation Error", "Status must be 'Approved' or 'Rejected'.")
            return
        
        try:
            query = "UPDATE Appointments SET Status=?, Message=? WHERE AppointmentID=?"
            self.db.execute_query(query, (status, message, appointment_id))
            messagebox.showinfo("Success", "Appointment status updated!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")

if __name__ == "__main__":
    db = DBConfig()
    root = tk.Tk()
    DonorRegistrationForm(root, db)
    root.mainloop()
