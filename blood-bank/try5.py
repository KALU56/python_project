import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from tkcalendar import DateEntry 
from tkinter import simpledialog

# Database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=KALKIDAN;'
    'DATABASE=BloodDonationSystem;'
    'UID=sa;'
    'PWD=kalkidan'
)
cursor = conn.cursor()

# Style configuration
BG_COLOR = "#ffe6e6"
BUTTON_COLOR = "#cc0000"
BUTTON_TEXT_COLOR = "white"
HEADER_COLOR = "#cc0000"
TEXT_COLOR = "#333333"
ENTRY_BG = "white"
TREE_HEADER_COLOR = "#ff6666"

class BloodDonationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donation System")
        self.root.configure(bg=BG_COLOR)
        self.style = ttk.Style()
        self._configure_styles()
        self.show_welcome_page()

    def _configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure("TButton", 
                           foreground=BUTTON_TEXT_COLOR,
                           background=BUTTON_COLOR,
                           font=("Arial", 10, "bold"),
                           padding=8,
                           relief="flat")
        self.style.map("TButton",
                      background=[("active", "#ff3333"), ("!active", BUTTON_COLOR)])
        self.style.configure("Header.TLabel",
                            font=("Arial", 18, "bold"),
                            foreground="white",
                            background=HEADER_COLOR,
                            padding=10)
        self.style.configure("Body.TLabel",
                            font=("Arial", 10),
                            background=BG_COLOR,
                            foreground=TEXT_COLOR)
        self.style.configure("TEntry",
                           fieldbackground=ENTRY_BG,
                           relief="flat",
                           padding=5)
        self.style.configure("Treeview.Heading",
                           font=("Arial", 10, "bold"),
                           background=TREE_HEADER_COLOR,
                           foreground="white")
        self.style.configure("Treeview",
                           background="white",
                           fieldbackground="white",
                           rowheight=25)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_header(self, title):
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text=title, style="Header.TLabel").pack()
        return header_frame

    def _create_content_frame(self):
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        return content_frame

    def show_welcome_page(self):
        self.clear_window()
        self._create_header("Welcome to Blood Donation System")
        content_frame = self._create_content_frame()
        
        btn_style = "TButton"
        ttk.Button(content_frame, text="Donor", command=self.donor_login_page, style=btn_style).pack(pady=10, fill="x")
        ttk.Button(content_frame, text="Supervisor", command=self.supervisor_login_page, style=btn_style).pack(pady=10, fill="x")

    # ================== DONOR SECTION ==================
    def donor_login_page(self):
        self.clear_window()
        self._create_header("Donor Login")
        content_frame = self._create_content_frame()
        
        fields = ["Username", "Password"]
        self.donor_entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=f"{field}:", style="Body.TLabel").pack(side="left", padx=5)
            entry = ttk.Entry(frame, style="TEntry", show="*" if "Password" in field else "")
            entry.pack(side="right", expand=True, fill="x", padx=5)
            self.donor_entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Login", command=self.donor_login, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Register", command=self.donor_register_page, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_welcome_page, style="TButton").pack(side="left", padx=5)

    def donor_login(self):
        username = self.donor_entries["Username"].get()
        password = self.donor_entries["Password"].get()
        
        cursor.execute("SELECT donor_id FROM Donors WHERE username=? AND password=?", (username, password))
        donor_id = cursor.fetchone()
        
        if donor_id:
            self.donor_activity_page(donor_id[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def donor_register_page(self):
        self.clear_window()
        self._create_header("Donor Registration")
        content_frame = self._create_content_frame()
        
        fields = [
            "Username", "Password", "First Name", "Last Name",
            "Date of Birth", "Gender", "Email", "Blood Type", "Phone Number"
        ]
        
        self.entries = {}
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=3, fill="x")
            ttk.Label(frame, text=f"{field}:", style="Body.TLabel").pack(side="left", padx=5)
            
            if field == "Gender":
                entry = ttk.Combobox(frame, values=["Male", "Female"], state="readonly")
            elif field == "Blood Type":
                blood_types = ['A', 'B', 'AB', 'A-', 'A+', 'B+', 'B-', 'AB-', 'AB+', 'O', 'O-', 'O+', 'None']
                entry = ttk.Combobox(frame, values=blood_types, state="readonly")
            elif field == "Date of Birth":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
            self.entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Submit", command=self.submit_registration, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.donor_login_page, style="TButton").pack(side="left", padx=5)

    def submit_registration(self):
        data = {k: v.get() for k, v in self.entries.items()}
        data["Date of Birth"] = data["Date of Birth"].strftime('%Y-%m-%d')

        if not (data["Phone Number"].startswith("09") or data["Phone Number"].startswith("07")) or len(data["Phone Number"]) != 10:
            messagebox.showerror("Error", "Invalid phone number")
            return
        
        try:
            cursor.execute("""
                INSERT INTO Donors (username, password, first_name, last_name, 
                date_of_birth, gender, email, blood_type, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["Username"], data["Password"], data["First Name"], data["Last Name"],
                data["Date of Birth"], data["Gender"], data["Email"] if data["Email"] else None,
                data["Blood Type"], data["Phone Number"]
            ))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
            self.donor_login_page()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def donor_activity_page(self, donor_id):
        self.clear_window()
        self.donor_id = donor_id
        self._create_header("Donor Activity Page")
        content_frame = self._create_content_frame()
        
        buttons = [
            ("Make Appointment", self.make_appointment),
            ("View Medical History", self.view_medical_history),
            ("View Health Status", self.view_health_status),
            ("Appointment Status", self.view_appointment_status),
            ("Logout", self.show_welcome_page)
        ]
        
        for text, command in buttons:
            ttk.Button(content_frame, text=text, command=command, style="TButton").pack(pady=5, fill="x")

    def make_appointment(self):
        window = tk.Toplevel(self.root)
        window.title("Make Appointment")
        window.configure(bg=BG_COLOR)
        content_frame = tk.Frame(window, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = ["Date", "Time (HH:MM)", "Message"]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=f"{field}:", style="Body.TLabel").pack(side="left", padx=5)
            
            if field == "Date":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
            entries[field] = entry
        
        def submit():
            try:
                appt_date = entries["Date"].get()
                appt_time = entries["Time (HH:MM)"].get()
                message = entries["Message"].get()
                
                datetime.strptime(appt_date, '%Y-%m-%d')
                datetime.strptime(appt_time, '%H:%M')
                
                if len(message) > 500:
                    raise ValueError("Message too long (max 500 characters)")
                
                # Insert appointment with Pending status
                cursor.execute("""
                    INSERT INTO Appointments (donor_id, appointment_date, appointment_time, message, status)
                    VALUES (?, ?, ?, ?, 'Pending')
                """, (self.donor_id, appt_date, appt_time, message))
                conn.commit()
                messagebox.showinfo("Success", "Appointment requested!")
                window.destroy()
                
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", f"Failed to create appointment:\n{str(e)}")
                conn.rollback()
        
        ttk.Button(content_frame, text="Submit", command=submit, style="TButton").pack(pady=10, fill="x")

    def view_appointment_status(self):
        try:
            cursor.execute("""
                SELECT appointment_date, appointment_time, message, status, supervisor_message 
                FROM Appointments 
                WHERE donor_id = ?
                ORDER BY appointment_date DESC
            """, (self.donor_id,))
            appointments = cursor.fetchall()
            
            window = tk.Toplevel(self.root)
            window.title("Appointment Status")
            window.configure(bg=BG_COLOR)
            
            main_frame = ttk.Frame(window)
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            columns = ("Date", "Time", "Your Message", "Status", "Supervisor Message")
            tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
            
            col_widths = [120, 80, 200, 100, 200]
            for col, width in zip(columns, col_widths):
                tree.heading(col, text=col)
                tree.column(col, width=width, anchor='w')
            
            vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=vsb.set)
            
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            
            if not appointments:
                tree.insert("", "end", values=("No appointments found", "", "", "", ""))
            else:
                for appt in appointments:
                    tree.insert("", "end", values=appt)
            
            main_frame.grid_rowconfigure(0, weight=1)
            main_frame.grid_columnconfigure(0, weight=1)
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load appointments:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def view_medical_history(self):
        cursor.execute("""
            SELECT entry_date, hiv_status, syphilis_status, hepatitis_status, sugar_level, outcome_message 
            FROM MedicalHistories WHERE donor_id=?
        """, (self.donor_id,))
        results = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("Medical History")
        window.configure(bg=BG_COLOR)
        window.state('zoomed')
        
        tree_frame = tk.Frame(window, bg=BG_COLOR)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        columns = ("Date", "HIV", "Syphilis", "Hepatitis", "Sugar", "Message")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center", stretch=tk.YES)
        
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
        window.configure(bg=BG_COLOR)
        window.state('zoomed')
        
        tree_frame = tk.Frame(window, bg=BG_COLOR)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        columns = ("Date", "Weight", "BP", "Sugar", "Start", "End")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center", stretch=tk.YES)
        
        for row in results:
            tree.insert("", "end", values=row)

    # ================== SUPERVISOR SECTION ==================
    def supervisor_login_page(self):
        self.clear_window()
        self._create_header("Supervisor Login")
        content_frame = self._create_content_frame()
        
        fields = ["Full Name", "Username", "Password"]
        self.sup_entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=f"{field}:", style="Body.TLabel").pack(side="left", padx=5)
            entry = ttk.Entry(frame, style="TEntry", show="*" if "Password" in field else "")
            entry.pack(side="right", expand=True, fill="x", padx=5)
            self.sup_entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Login", command=self.supervisor_login, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_welcome_page, style="TButton").pack(side="left", padx=5)

    def supervisor_login(self):
        data = {k: v.get() for k, v in self.sup_entries.items()}
        
        cursor.execute("""
            SELECT supervisor_id FROM Supervisors 
            WHERE full_name=? AND username=? AND password=?
        """, (data["Full Name"], data["Username"], data["Password"]))
        supervisor_id = cursor.fetchone()
        
        if supervisor_id:
            self.supervisor_activity_page(supervisor_id[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def supervisor_activity_page(self, supervisor_id):
        self.clear_window()
        self.supervisor_id = supervisor_id
        self._create_header("Supervisor Activity Page")
        content_frame = self._create_content_frame()
        
        buttons = [
            ("View Donors", self.view_donors),
            ("Appointment Confirmations", self.view_appointments),
            ("Send Medical History", self.send_medical_history),
            ("Send Health Status", self.send_health_status),
            ("Logout", self.show_welcome_page)
        ]
        
        for text, command in buttons:
            ttk.Button(content_frame, text=text, command=command, style="TButton").pack(pady=5, fill="x")

    def view_donors(self):
        cursor.execute("SELECT * FROM Donors")
        results = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title("All Donors")
        window.configure(bg=BG_COLOR)
        
        tree_frame = tk.Frame(window, bg=BG_COLOR)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        columns = [column[0] for column in cursor.description]
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        for row in results:
            formatted_row = list(row)
            formatted_row[5] = str(formatted_row[5])
            tree.insert("", "end", values=formatted_row)

    def view_appointments(self):
        window = tk.Toplevel(self.root)
        window.title("Pending Appointments")
        window.configure(bg=BG_COLOR)
        
        def refresh_appointments():
            cursor.execute("""
                SELECT a.appointment_id, d.username, a.appointment_date, 
                       a.appointment_time, a.message, a.status 
                FROM Appointments a
                JOIN Donors d ON a.donor_id = d.donor_id
                WHERE a.status = 'Pending'
            """)
            appointments = cursor.fetchall()
            
            for item in tree.get_children():
                tree.delete(item)
            for appt in appointments:
                tree.insert("", "end", values=appt)
        
        main_frame = ttk.Frame(window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Donor", "Date", "Time", "Message", "Status")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        
        col_widths = [50, 100, 100, 80, 250, 100]
        for col, width in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor='w')
        
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        
        # Status update controls
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Label(status_frame, text="Select Status:").pack(side=tk.LEFT, padx=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(status_frame, textvariable=status_var, 
                                  values=["Approved", "Rejected"], state="readonly")
        status_combo.pack(side=tk.LEFT, padx=5)
        
        def handle_status_change():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select an appointment first!")
                return
            
            new_status = status_var.get()
            appt_id = tree.item(selected[0])["values"][0]
            
            # Get donor details
            cursor.execute("SELECT donor_id FROM Appointments WHERE appointment_id=?", (appt_id,))
            donor_id_result = cursor.fetchone()
            if not donor_id_result:
                messagebox.showerror("Error", "Appointment not found")
                return
            
            donor_id = donor_id_result[0]
            supervisor_message = ""
            
            if new_status == "Rejected":
                supervisor_message = simpledialog.askstring("Reason", "Enter rejection reason:")
                if not supervisor_message:
                    return
            elif new_status == "Approved":
                # Check donor age
                cursor.execute("SELECT date_of_birth FROM Donors WHERE donor_id=?", (donor_id,))
                dob_result = cursor.fetchone()
                if not dob_result:
                    messagebox.showerror("Error", "Donor not found")
                    return
                
                dob = dob_result[0]
                today = datetime.today().date()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                
                if age < 18:
                    messagebox.showerror("Error", "Donor must be at least 18 years old")
                    return
                supervisor_message = "Approved for donation"

            try:
                cursor.execute("""
                    UPDATE Appointments 
                    SET status = ?, supervisor_message = ?
                    WHERE appointment_id = ?
                """, (new_status, supervisor_message, appt_id))
                conn.commit()
                messagebox.showinfo("Success", f"Appointment {new_status.lower()}")
                refresh_appointments()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                conn.rollback()
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Refresh", command=refresh_appointments).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Status", command=handle_status_change).pack(side=tk.LEFT, padx=5)
        
        refresh_appointments()
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def send_medical_history(self):
        window = tk.Toplevel(self.root)
        window.title("Send Medical History")
        window.configure(bg=BG_COLOR)
        content_frame = tk.Frame(window, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            "Donor Username", "Entry Date", "HIV Status", 
            "Syphilis Status", "Hepatitis Status", "Sugar Level", "Outcome Message"
        ]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=3, fill="x")
            ttk.Label(frame, text=f"{field}:", style="Body.TLabel").pack(side="left", padx=5)
            
            if field in ["HIV Status", "Syphilis Status", "Hepatitis Status"]:
                entry = ttk.Combobox(frame, values=["Positive", "Negative"], state="readonly")
            elif field == "Entry Date":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
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
                    entries["Entry Date"].get(),
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
        
        ttk.Button(content_frame, text="Submit", command=submit, style="TButton").pack(pady=10, fill="x")

    def send_health_status(self):
        window = tk.Toplevel(self.root)
        window.title("Send Health Status")
        window.configure(bg=BG_COLOR)
        content_frame = tk.Frame(window, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            "Donor Username", "Donation Date", "Weight", 
            "Blood Pressure", "Sugar Level", "Start Time (HH:MM)", "End Time (HH:MM)"
        ]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=3, fill="x")
            ttk.Label(frame, text=f"{field}:", style="Body.TLabel").pack(side="left", padx=5)
            
            if field == "Donation Date":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
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
                    entries["Donation Date"].get(),
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
        
        ttk.Button(content_frame, text="Submit", command=submit, style="TButton").pack(pady=10, fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.minsize(800, 600)
    app = BloodDonationSystem(root)
    root.mainloop()