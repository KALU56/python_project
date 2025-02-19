import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

# Database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=KALKIDAN;'
    'DATABASE=BloodDonationSystem;'
    'UID=sa;'
    'PWD=kalkidan'
)
cursor = conn.cursor()

class BloodDonationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donation System")
        self.show_welcome_page()
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_welcome_page(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Blood Donation System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Donor", command=self.donor_login_page, width=20).pack(pady=10)
        tk.Button(self.root, text="Supervisor", command=self.supervisor_login_page, width=20).pack(pady=10)

    # Donor related functions
    def donor_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Donor Login", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Username:").pack()
        self.donor_username = tk.Entry(self.root)
        self.donor_username.pack()
        
        tk.Label(self.root, text="Password:").pack()
        self.donor_password = tk.Entry(self.root, show="*")
        self.donor_password.pack()
        
        tk.Button(self.root, text="Login", command=self.donor_login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.donor_register_page).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_welcome_page).pack(pady=5)

    def donor_login(self):
        username = self.donor_username.get()
        password = self.donor_password.get()
        
        cursor.execute("SELECT donor_id FROM Donors WHERE username=? AND password=?", (username, password))
        donor_id = cursor.fetchone()
        
        if donor_id:
            self.donor_activity_page(donor_id[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def donor_register_page(self):
        self.clear_window()
        tk.Label(self.root, text="Donor Registration", font=("Arial", 14)).pack(pady=10)
        
        fields = [
            ("Username", "entry"), ("Password", "entry"),
            ("First Name", "entry"), ("Last Name", "entry"),
            ("Date of Birth (YYYY-MM-DD)", "entry"), 
            ("Gender (Male/Female)", "entry"), ("Email", "entry"),
            ("Blood Type", "entry"), ("Phone Number", "entry")
        ]
        
        self.entries = {}
        for field, widget_type in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.entries[field] = entry
        
        tk.Button(self.root, text="Submit", command=self.submit_registration).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.donor_login_page).pack(pady=5)

    def submit_registration(self):
        data = {k: v.get() for k, v in self.entries.items()}
        
        # Validation
        if not (data["Phone Number"].startswith("09") or data["Phone Number"].startswith("07")) or len(data["Phone Number"]) != 10:
            messagebox.showerror("Error", "Invalid phone number")
            return
        
        try:
            cursor.execute("""
                INSERT INTO Donors (username, password, first_name, last_name, date_of_birth, gender, email, blood_type, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["Username"], data["Password"], data["First Name"], data["Last Name"],
                data["Date of Birth (YYYY-MM-DD)"], data["Gender (Male/Female)"], 
                data["Email"] if data["Email"] else None, data["Blood Type"], data["Phone Number"]
            ))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
            self.donor_login_page()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def donor_activity_page(self, donor_id):
        self.clear_window()
        self.donor_id = donor_id
        tk.Label(self.root, text="Donor Activity Page", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.root, text="Make Appointment", command=self.make_appointment).pack(pady=10)
        tk.Button(self.root, text="View Medical History", command=self.view_medical_history).pack(pady=10)
        tk.Button(self.root, text="View Health Status", command=self.view_health_status).pack(pady=10)
        tk.Button(self.root, text="Appointment Status", command=self.view_appointment_status).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.show_welcome_page).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.show_welcome_page).pack(pady=10)

    def make_appointment(self):
        window = tk.Toplevel(self.root)
        window.title("Make Appointment")
        
        tk.Label(window, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        date_entry = tk.Entry(window)
        date_entry.grid(row=0, column=1)
        
        tk.Label(window, text="Time (HH:MM):").grid(row=1, column=0)
        time_entry = tk.Entry(window)
        time_entry.grid(row=1, column=1)
        
        tk.Label(window, text="Message:").grid(row=2, column=0)
        message_entry = tk.Entry(window)
        message_entry.grid(row=2, column=1)
        
        def submit():
        # Include status explicitly
            cursor.execute("""
                INSERT INTO Appointments (donor_id, appointment_date, appointment_time, message, status)
                VALUES (?, ?, ?, ?, 'Pending')
            """, (self.donor_id, date_entry.get(), time_entry.get(), message_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Appointment created. Please check status later.")
            window.destroy()
        
        tk.Button(window, text="Submit", command=submit).grid(row=3, columnspan=2)
    def view_appointment_status(self):
        cursor.execute("""
            SELECT appointment_date, appointment_time, message, status 
            FROM Appointments 
            WHERE donor_id = ?
        """, (self.donor_id,))
        appointments = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("Appointment Status")
        
        columns = ("Date", "Time", "Message", "Status")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(padx=10, pady=10)
        
        for appt in appointments:
            tree.insert("", "end", values=appt)
    def view_medical_history(self):
        cursor.execute("""
            SELECT entry_date, hiv_status, syphilis_status, hepatitis_status, sugar_level, outcome_message 
            FROM MedicalHistories WHERE donor_id=?
        """, (self.donor_id,))
        results = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("Medical History")
        
        tree = ttk.Treeview(window, columns=("Date", "HIV", "Syphilis", "Hepatitis", "Sugar", "Message"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack()
        
        for row in results:
            tree.insert("", "end", values=row)
    def view_health_status(self):
        cursor.execute("""
            SELECT donation_date, weight, blood_pressure, sugar_level, start_time, end_time 
            FROM HealthStatuses WHERE donor_id=?
        """, (self.donor_id,))
        results = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("Health Status")
        
        tree = ttk.Treeview(window, columns=("Date", "Weight", "BP", "Sugar", "Start", "End"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack()
        
        for row in results:
            tree.insert("", "end", values=row)            

    # Supervisor related functions
    def supervisor_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Supervisor Login", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Full Name:").pack()
        self.sup_fullname = tk.Entry(self.root)
        self.sup_fullname.pack()
        
        tk.Label(self.root, text="Username:").pack()
        self.sup_username = tk.Entry(self.root)
        self.sup_username.pack()
        
        tk.Label(self.root, text="Password:").pack()
        self.sup_password = tk.Entry(self.root, show="*")
        self.sup_password.pack()
        
        tk.Button(self.root, text="Login", command=self.supervisor_login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_welcome_page).pack(pady=5)

    def supervisor_login(self):
        fullname = self.sup_fullname.get()
        username = self.sup_username.get()
        password = self.sup_password.get()
        
        cursor.execute("""
            SELECT supervisor_id FROM Supervisors 
            WHERE full_name=? AND username=? AND password=?
        """, (fullname, username, password))
        supervisor_id = cursor.fetchone()
        
        if supervisor_id:
            self.supervisor_activity_page(supervisor_id[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def supervisor_activity_page(self, supervisor_id):
        self.clear_window()
        self.supervisor_id = supervisor_id
        
        tk.Label(self.root, text="Supervisor Activity Page", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View Donors", command=self.view_donors).pack(pady=10)
        tk.Button(self.root, text="Appointment Confirmations", command=self.view_appointments).pack(pady=10)
        tk.Button(self.root, text="Send Medical History", command=self.send_medical_history).pack(pady=10)  # Must exist
        tk.Button(self.root, text="Send Health Status", command=self.send_health_status).pack(pady=10) 
             # Must exist
        tk.Button(self.root, text="Logout", command=self.show_welcome_page).pack(pady=10)

    def view_donors(self):
        
        cursor.execute("SELECT * FROM Donors")
        results = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("All Donors")
        
        columns = [column[0] for column in cursor.description]
        tree = ttk.Treeview(window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()
        
        for row in results:
            tree.insert("", "end", values=row)
    def view_appointments(self):
        cursor.execute("""
            SELECT a.appointment_id, d.username, a.appointment_date, 
                   a.appointment_time, a.message 
            FROM Appointments a
            JOIN Donors d ON a.donor_id = d.donor_id
            WHERE a.status = 'Pending'
        """)
        appointments = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("Pending Appointments")
        
        columns = ("ID", "Donor", "Date", "Time", "Message")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
        for appt in appointments:
            tree.insert("", "end", values=appt)
        
        # Add both approve and reject buttons
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def approve_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select an appointment first!")
                return
            
            appt_id = tree.item(selected[0])["values"][0]
            
            cursor.execute("""
                UPDATE Appointments 
                SET status = 'Approved' 
                WHERE appointment_id = ?
            """, (appt_id,))
            conn.commit()
            
            messagebox.showinfo("Approved", "Thank you for volunteering! Your appointment is approved.")
            tree.delete(selected[0])
        
        def reject_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select an appointment first!")
                return
            
            appt_id = tree.item(selected[0])["values"][0]
            
            cursor.execute("""
                UPDATE Appointments 
                SET status = 'Rejected' 
                WHERE appointment_id = ?
            """, (appt_id,))
            conn.commit()
            
            messagebox.showinfo("Rejected", "Sorry, this time is not available. Please ask the donor to choose another time.")
            tree.delete(selected[0])
        
        tk.Button(btn_frame, text="Approve", command=approve_appointment).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reject", command=reject_appointment).pack(side=tk.LEFT, padx=5)


    def send_medical_history(self):
        window = tk.Toplevel(self.root)
        window.title("Send Medical History")
        
        fields = [
            ("Donor Username", "entry"), ("Entry Date (YYYY-MM-DD)", "entry"),
            ("HIV Status", "entry"), ("Syphilis Status", "entry"),
            ("Hepatitis Status", "entry"), ("Sugar Level", "entry"),
            ("Outcome Message", "entry")
        ]
        
        entries = {}
        for i, (field, _) in enumerate(fields):
            tk.Label(window, text=field).grid(row=i, column=0)
            entry = tk.Entry(window)
            entry.grid(row=i, column=1)
            entries[field] = entry
        
        def submit():
            donor_username = entries["Donor Username"].get()
            cursor.execute("SELECT donor_id FROM Donors WHERE username=?", (donor_username,))
            donor_id = cursor.fetchone()
            
            if not donor_id:
                messagebox.showerror("Error", "Invalid donor username")
                return
            
            try:
                cursor.execute("""
                    INSERT INTO MedicalHistories (donor_id, supervisor_id, entry_date, 
                    hiv_status, syphilis_status, hepatitis_status, sugar_level, outcome_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    donor_id[0], self.supervisor_id,
                    entries["Entry Date (YYYY-MM-DD)"].get(),
                    entries["HIV Status"].get(),
                    entries["Syphilis Status"].get(),
                    entries["Hepatitis Status"].get(),
                    entries["Sugar Level"].get(),
                    entries["Outcome Message"].get()
                ))
                conn.commit()
                messagebox.showinfo("Success", "Medical history added")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(window, text="Submit", command=submit).grid(row=len(fields), columnspan=2)

    def send_health_status(self):
        window = tk.Toplevel(self.root)
        window.title("Send Health Status")
        
        fields = [
            ("Donor Username", "entry"), 
            ("Donation Date (YYYY-MM-DD)", "entry"),
            ("Weight", "entry"), 
            ("Blood Pressure", "entry"),
            ("Sugar Level", "entry"), 
            ("Start Time (HH:MM)", "entry"),
            ("End Time (HH:MM)", "entry")
        ]
        
        entries = {}
        for i, (field, _) in enumerate(fields):
            tk.Label(window, text=field).grid(row=i, column=0)
            entry = tk.Entry(window)
            entry.grid(row=i, column=1)
            entries[field] = entry
        
        def submit():
            donor_username = entries["Donor Username"].get()
            cursor.execute("SELECT donor_id FROM Donors WHERE username=?", (donor_username,))
            donor_id = cursor.fetchone()
            
            if not donor_id:
                messagebox.showerror("Error", "Invalid donor username")
                return
            
            try:
                cursor.execute("""
                    INSERT INTO HealthStatuses (
                        donor_id, supervisor_id, donation_date, 
                        weight, blood_pressure, sugar_level, 
                        start_time, end_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    donor_id[0], self.supervisor_id,
                    entries["Donation Date (YYYY-MM-DD)"].get(),
                    entries["Weight"].get(),
                    entries["Blood Pressure"].get(),
                    entries["Sugar Level"].get(),
                    entries["Start Time (HH:MM)"].get(),
                    entries["End Time (HH:MM)"].get()
                ))
                conn.commit()
                messagebox.showinfo("Success", "Health status added")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(window, text="Submit", command=submit).grid(row=len(fields), columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = BloodDonationSystem(root)
    root.mainloop()