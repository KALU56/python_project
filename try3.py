import tkinter as tk
from tkinter import messagebox, scrolledtext
import uuid
import re
from datetime import datetime
import pyodbc

# Database Configuration
def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=KALKIDAN;'
        'DATABASE=BloodBankDB;'
        'UID=sa;'
        'PWD=kalkidan'
    )

class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System")
        self.root.geometry("400x300")

        tk.Label(root, text="Welcome to Blood Bank System", font=("Helvetica", 14)).pack(pady=20)
        
        buttons = [
            ("Donor Portal", self.go_to_donor),
            ("Supervisor Portal", self.go_to_supervisor),
            ("Exit", self.root.quit)
        ]
        
        for text, cmd in buttons:
            tk.Button(root, text=text, font=("Helvetica", 12), command=cmd).pack(pady=5)

    def go_to_donor(self):
        donor_window = tk.Toplevel(self.root)
        DonorPortal(donor_window)

    def go_to_supervisor(self):
        supervisor_window = tk.Toplevel(self.root)
        SupervisorPortal(supervisor_window)

class DonorPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Portal")
        self.root.geometry("400x300")
        
        tk.Label(root, text="Donor Portal", font=("Helvetica", 14)).pack(pady=20)
        
        options = [
            ("Registration", DonorRegistrationForm),
            ("Login", DonorLoginForm),
            ("Exit", root.destroy)
        ]
        
        for text, cmd in options:
            tk.Button(root, text=text, font=("Helvetica", 12), 
                    command=lambda c=cmd: c(tk.Toplevel(root)) if c != root.destroy else c()).pack(pady=5)

class DonorRegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Registration")
        self.root.geometry("500x600")
        
        fields = [
            ("Username:", "username"),
            ("Password:", "password"),
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Date of Birth (YYYY-MM-DD):", "dob"),
            ("Gender (Male/Female):", "gender"),
            ("Blood Type:", "blood_type"),
            ("Email (optional):", "email"),
            ("Phone Number:", "phone")
        ]
        
        self.entries = {}
        for text, name in fields:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            tk.Label(frame, text=text).pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            self.entries[name] = entry

        tk.Button(self.root, text="Submit", command=self.validate_and_register).pack(pady=20)

    def validate_and_register(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        required = ['username', 'password', 'first_name', 'last_name', 'dob', 'gender', 'blood_type', 'phone']
        
        if any(not data[k] for k in required):
            messagebox.showerror("Error", "All required fields must be filled")
            return

        if not self.validate_date(data['dob']):
            messagebox.showerror("Error", "Invalid date format or age < 18 (YYYY-MM-DD)")
            return

        if not re.match(r"^(09|07)\d{8}$", data['phone']):
            messagebox.showerror("Error", "Invalid phone number format")
            return

        if data['email'] and not re.match(r"^[\w.+-]+@gmail\.com$", data['email']):
            messagebox.showerror("Error", "Invalid email format (Gmail only)")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Donors 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                data['username'],
                data['password'],
                data['first_name'],
                data['last_name'],
                data['dob'],
                data['gender'],
                data['blood_type'] if data['blood_type'] else None,  # Handle optional
                data['email'],
                data['phone']
            ))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()
        except pyodbc.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if 'conn' in locals():
                conn.close()

    def validate_date(self, dob):
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            return (datetime.now() - birth_date).days >= 18*365
        except ValueError:
            return False

class DonorLoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Login")
        self.root.geometry("300x200")
        
        tk.Label(root, text="Username:").pack(pady=5)
        self.username = tk.Entry(root)
        self.username.pack()
        
        tk.Label(root, text="Password:").pack(pady=5)
        self.password = tk.Entry(root, show="*")
        self.password.pack()
        
        tk.Button(root, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DonorID FROM Donors 
                WHERE Username = ? AND Password = ?
            """, (self.username.get(), self.password.get()))
            
            if donor := cursor.fetchone():
                self.open_donor_activity(donor[0])
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def open_donor_activity(self, donor_id):
        activity_window = tk.Toplevel(self.root)
        activity_window.title("Donor Activities")
        tk.Button(activity_window, text="Health States", 
                 command=lambda: HealthStatesViewer(activity_window, donor_id)).pack(pady=5)
        tk.Button(activity_window, text="Medical History", 
                 command=lambda: MedicalHistoryViewer(activity_window, donor_id)).pack(pady=5)
        tk.Button(activity_window, text="Schedule Appointment", 
                 command=lambda: AppointmentScheduler(activity_window, donor_id)).pack(pady=5)
        tk.Button(activity_window, text="Exit", command=activity_window.destroy).pack(pady=5)
class HealthStatesViewer:
    def __init__(self, root, donor_id):
        self.root = root
        self.root.title("Health States")
        self.root.geometry("600x400")
        
        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        text_area.pack(expand=True, fill="both")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT CheckDate, Weight, BloodPressure, SugarLevel, StartTime, EndTime 
                FROM HealthStates 
                WHERE DonorID = ?
            """, (donor_id,))
            
            for record in cursor.fetchall():
                text_area.insert(tk.END, f"Date: {record.CheckDate}\n")
                text_area.insert(tk.END, f"Weight: {record.Weight} kg\n")
                text_area.insert(tk.END, f"Blood Pressure: {record.BloodPressure}\n")
                text_area.insert(tk.END, f"Sugar Level: {record.SugarLevel}\n")
                text_area.insert(tk.END, f"Start Time: {record.StartTime}\n")
                text_area.insert(tk.END, f"End Time: {record.EndTime}\n")
                text_area.insert(tk.END, "-"*50 + "\n\n")
            
            text_area.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
class MedicalHistoryViewer:
    def __init__(self, root, donor_id):
        self.root = root
        self.root.title("Medical History")
        self.root.geometry("600x400")
        
        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        text_area.pack(expand=True, fill="both")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Date, HIV, Syphilis, HepatitisB, HepatitisC, SugarLevel, OutcomeDetails 
                FROM MedicalHistory 
                WHERE DonorID = ?
            """, (donor_id,))
            
            for record in cursor.fetchall():
                text_area.insert(tk.END, f"Date: {record.Date}\n")
                text_area.insert(tk.END, f"HIV: {'Positive' if record.HIV else 'Negative'}\n")
                text_area.insert(tk.END, f"Syphilis: {'Positive' if record.Syphilis else 'Negative'}\n")
                text_area.insert(tk.END, f"Hepatitis B: {'Positive' if record.HepatitisB else 'Negative'}\n")
                text_area.insert(tk.END, f"Hepatitis C: {'Positive' if record.HepatitisC else 'Negative'}\n")
                text_area.insert(tk.END, f"Sugar Level: {record.SugarLevel}\n")
                text_area.insert(tk.END, f"Outcome: {record.OutcomeDetails}\n")
                text_area.insert(tk.END, "-"*50 + "\n\n")
            
            text_area.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

class AppointmentScheduler:
    def __init__(self, root, donor_id):
        self.root = root
        self.donor_id = donor_id
        self.root.title("Schedule Appointment")
        self.root.geometry("300x250")
        
        tk.Label(root, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.date = tk.Entry(root)
        self.date.pack()
        
        tk.Label(root, text="Time (HH:MM):").pack(pady=5)
        self.time = tk.Entry(root)
        self.time.pack()
        tk.Label(root, text="Additional Notes:").pack(pady=5)
        self.notes = tk.Entry(root)
        self.notes.pack()

        tk.Button(root, text="Submit", command=self.schedule).pack(pady=10)

    def schedule(self):
        try:
            datetime_str = f"{self.date.get()} {self.time.get()}"
            appointment_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            if appointment_time < datetime.now():
                messagebox.showerror("Error", "Cannot schedule past appointments")
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Appointments (DonorID, AppointmentDateTime, Status, Message)
                VALUES (?, ?, 'Pending')
            """, (self.donor_id, appointment_time,self.notes.get()))
            conn.commit()
            messagebox.showinfo("Success", "Appointment scheduled!")
            self.root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid datetime format")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

class SupervisorPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Supervisor Portal")
        self.root.geometry("400x300")
        
        tk.Label(root, text="Supervisor Portal", font=("Helvetica", 14)).pack(pady=20)
        
        options = [
            ("View Donors", self.view_donors),
            ("Manage Appointments", self.manage_appointments),
            ("Health Check Entry", self.health_check_entry),
            ("Exit", root.destroy)
        ]
        
        for text, cmd in options:
            tk.Button(root, text=text, font=("Helvetica", 12), command=cmd).pack(pady=5)

    def view_donors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Donors")
            
            donors_window = tk.Toplevel(self.root)
            text_area = scrolledtext.ScrolledText(donors_window, wrap=tk.WORD)
            text_area.pack(expand=True, fill="both")
            
            for donor in cursor.fetchall():
                text_area.insert(tk.END, f"Donor ID: {donor.DonorID}\n")
                text_area.insert(tk.END, f"Name: {donor.FirstName} {donor.LastName}\n")
                text_area.insert(tk.END, f"Blood Type: {donor.BloodType}\n")
                text_area.insert(tk.END, "-"*50 + "\n\n")
            
            text_area.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def manage_appointments(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.AppointmentID, d.Username, a.AppointmentDateTime, a.Status 
                FROM Appointments a
                JOIN Donors d ON a.DonorID = d.DonorID
                WHERE a.Status = 'Pending'
            """)
            
            window = tk.Toplevel(self.root)
            window.title("Pending Appointments")
            
            for appointment in cursor.fetchall():
                frame = tk.Frame(window)
                frame.pack(pady=5)
                
                tk.Label(frame, text=f"{appointment.Username} - {appointment.AppointmentDateTime}").pack(side=tk.LEFT)
                
                msg_frame = tk.Frame(frame)
                msg_frame.pack(side=tk.LEFT)
                tk.Label(msg_frame, text="Message:").pack()
                message_entry = tk.Entry(msg_frame)
                message_entry.pack()
                
                tk.Button(frame, text="Approve", 
                         command=lambda id=appointment.AppointmentID, e=message_entry: 
                         self.update_status(id, "Approved", e.get())).pack(side=tk.LEFT)
                tk.Button(frame, text="Reject", 
                         command=lambda id=appointment.AppointmentID, e=message_entry: 
                         self.update_status(id, "Disapproved", e.get())).pack(side=tk.LEFT)
        except Exception as e:
                messagebox.showerror("Database Error", str(e))
        finally:
                conn.close()

    def update_status(self, appointment_id, status):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Appointments 
                SET Status = ?, Message = ?
                WHERE AppointmentID = ?
            """, (status, message, appointment_id))
            conn.commit()
            messagebox.showinfo("Success", "Appointment status updated")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
    def health_check_entry(self):
        window = tk.Toplevel(self.root)
        window.title("Health Check Entry")
        
        fields = [
            ("Donor Username:", "username"),
            ("Weight (kg):", "weight"),
            ("Blood Pressure:", "bp"),
            ("Sugar Level:", "sugar"),
            ("Start Time (YYYY-MM-DD HH:MM):", "start"),
            ("End Time (YYYY-MM-DD HH:MM):", "end")
        ]
        
        self.health_entries = {}
        for text, name in fields:
            frame = tk.Frame(window)
            frame.pack(pady=5)
            tk.Label(frame, text=text).pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            self.health_entries[name] = entry

        tk.Button(window, text="Submit", command=self.submit_health_check).pack(pady=10)

    def submit_health_check(self):
        data = {k: v.get() for k, v in self.health_entries.items()}
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get DonorID from username
            cursor.execute("SELECT DonorID FROM Donors WHERE Username = ?", (data['username'],))
            if donor := cursor.fetchone():
                donor_id = donor[0]
                
                cursor.execute("""
                    INSERT INTO HealthStates 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    donor_id,
                    data['weight'],
                    data['bp'],
                    data['sugar'],
                    data['start'],
                    data['end']
                ))
                conn.commit()
                messagebox.showinfo("Success", "Health check recorded")
            else:
                messagebox.showerror("Error", "Donor not found")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
if __name__ == "__main__":
    root = tk.Tk()
    WelcomePage(root)
    root.mainloop()