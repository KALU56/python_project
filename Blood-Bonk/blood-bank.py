import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from tkcalendar import DateEntry
import datetime
from decimal import Decimal
# Database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=KALKIDAN;'
    'DATABASE=BloodDonationSystem;'
    'UID=sa;'
    'PWD=kalkidan'
)
cursor = conn.cursor()

# Language configurations
LANGUAGES = {
    'en': {
        'welcome': "Welcome to Blood Donation System",
        'donor': "Donor",
        'supervisor': "Supervisor",
        'login': "Login",
        'register': "Register",
        'back': "Back",
        'username': "Username",
        'password': "Password",
        'first_name': "First Name",
        'last_name': "Last Name",
        'date_of_birth': "Date of Birth",
        'gender': "Gender",
        'email': "Email",
        'blood_type': "Blood Type",
        'phone_number': "Phone Number",
        'submit': "Submit",
        'male': "Male",
        'female': "Female",
        'invalid_phone': "Invalid phone number (must start with 09/07 and 10 digits)",
        'registration_success': "Registration successful",
        'make_appointment': "Make Appointment",
        'view_medical_history': "View Medical History",
        'view_health_status': "View Health Status",
        'logout': "Logout",
        'invalid_credentials': "Invalid credentials",
        'appointment_date': "Date",
        'appointment_time': "Time (HH:MM)",
        'appointment_message': "Message",
        'appointment_success': "Appointment requested!",
        'medical_history': "Medical History",
        'health_status': "Health Status",
        'full_name': "Full Name",
        'entry_date': "Entry Date",
        'hiv_status': "HIV Status",
        'syphilis_status': "Syphilis Status",
        'hepatitis_status': "Hepatitis Status",
        'sugar_level': "Sugar Level",
        'outcome_message': "Outcome Message",
        'donation_date': "Donation Date",
        'weight': "Weight",
        'blood_pressure': "Blood Pressure",
        'start_time': "Start Time",
        'end_time': "End Time",
        'positive': "Positive",
        'negative': "Negative",
        'none': "None",
        'donor_login': "Donor Login",
        'donor_registration': "Donor Registration",
        'supervisor_login': "Supervisor Login",
        'view_donors': "View Donors",
        'send_medical_history': "Send Medical History",
        'send_health_status': "Send Health Status",
    },
    'am': {
        'welcome': "እንኳን ወደ ደም ባንክ በደህና መጡ",
        'donor': "ደም ለጋሽ",
        'supervisor': "ተቆጣጣሪ",
        'login': "ግባ",
        'register': "ይመዝገቡ",
        'back': "ተመለስ",
        'username': "የተጠቃሚ ስም",
        'password': "የይለፍ ቃል",
        'first_name': "ስም",
        'last_name': "የአባት ስም",
        'date_of_birth': "የትውልድ ቀን",
        'gender': "ጾታ",
        'email': "ኢሜይል",
        'blood_type': "የደም አይነት",
        'phone_number': "ስልክ ቁጥር",
        'submit': "አስገባ",
        'male': "ወንድ",
        'female': "ሴት",
        'invalid_phone': "ትክክል ያልሆነ ስልክ ቁጥር (በ09 ወይም 07 ይጀምር እና 10 አሃዞች ይኑሩት)",
        'registration_success': "ምዝገባ በትክክል ተከናውኗል",
        'make_appointment': "ቀጠሮ ይያዙ",
        'view_medical_history': "የሕክምና ታሪክ ይመልከቱ",
        'view_health_status': "የጤና ሁኔታ ይመልከቱ",
        'logout': "ውጣ",
        'invalid_credentials': "ትክክል ያልሆኑ ማረጋገጫዎች",
        'appointment_date': "ቀን",
        'appointment_time': "ጊዜ (ሰአት:ደቂቃ)",
        'appointment_message': "መልእክት",
        'appointment_success': "ቀጠሮዎ በትክክል ቀርቧል!",
        'medical_history': "የሕክምና ታሪክ",
        'health_status': "የጤና ሁኔታ",
        'full_name': "ሙሉ ስም",
        'entry_date': "የገባበት ቀን",
        'hiv_status': "ኤች አይ ቪ ሁኔታ",
        'syphilis_status': "ሲፊሊስ ሁኔታ",
        'hepatitis_status': "ሄፓታይትስ ሁኔታ",
        'sugar_level': "ሽኩርት መጠን",
        'outcome_message': "ውጤት መልእክት",
        'donation_date': "የደም ልገሳ ቀን",
        'weight': "ክብደት",
        'blood_pressure': "የደም ግፊት",
        'start_time': "የጀመረበት ጊዜ",
        'end_time': "ያለቀበት ጊዜ",
        'positive': "አዎንታዊ",
        'negative': "አሉታዊ",
        'none': "የለም",
        'donor_login': "ደም ለጋሽ መግቢያ",
        'donor_registration': "ደም ለጋሽ ምዝገባ",
        'supervisor_login': "ተቆጣጣሪ መግቢያ",
        'view_donors': "ደም ለጋሾችን ይመልከቱ",
        'send_medical_history': "የሕክምና ታሪክ ላክ",
        'send_health_status': "የጤና ሁኔታ ላክ",
    }
}


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
        self.current_language = 'en'
        self.style = ttk.Style()
        self._configure_styles()
        self.show_welcome_page()

    def tr(self, key):
        return LANGUAGES[self.current_language].get(key, key)

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

    def _create_header(self, title_key):
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text=self.tr(title_key), style="Header.TLabel").pack()
        return header_frame

    def _create_content_frame(self):
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        return content_frame

    def show_welcome_page(self):
        self.clear_window()
        self._create_header('welcome')
        content_frame = self._create_content_frame()
        
        # Language selection
        lang_frame = tk.Frame(content_frame, bg=BG_COLOR)
        lang_frame.pack(pady=10)
        ttk.Label(lang_frame, text="Language:", style="Body.TLabel").pack(side=tk.LEFT)
        lang_combo = ttk.Combobox(lang_frame, values=['English', 'አማርኛ'], state="readonly")
        lang_combo.current(0 if self.current_language == 'en' else 1)
        lang_combo.pack(side=tk.LEFT, padx=10)
        
        def change_language(event):
            self.current_language = 'en' if lang_combo.get() == 'English' else 'am'
            self.show_welcome_page()
            
        lang_combo.bind("<<ComboboxSelected>>", change_language)

        btn_style = "TButton"
        ttk.Button(content_frame, text=self.tr('donor'), command=self.donor_login_page, 
                 style=btn_style).pack(pady=10, fill="x")
        ttk.Button(content_frame, text=self.tr('supervisor'), command=self.supervisor_login_page, 
                 style=btn_style).pack(pady=10, fill="x")

    # ================== DONOR SECTION ==================
    def donor_login_page(self):
        self.clear_window()
        self._create_header("donor_login")
        content_frame = self._create_content_frame()
        
        fields = ["username", "password"]
        self.donor_entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=self.tr(field)+":", style="Body.TLabel").pack(side="left", padx=5)
            entry = ttk.Entry(frame, style="TEntry", show="*" if field == "password" else "")
            entry.pack(side="right", expand=True, fill="x", padx=5)
            self.donor_entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text=self.tr('login'), command=self.donor_login, 
                 style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text=self.tr('register'), command=self.donor_register_page, 
                 style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text=self.tr('back'), command=self.show_welcome_page, 
                 style="TButton").pack(side="left", padx=5)

    def donor_login(self):
        username = self.donor_entries["username"].get()
        password = self.donor_entries["password"].get()
        
        cursor.execute("SELECT donor_id FROM Donors WHERE username=? AND password=?", (username, password))
        donor_id = cursor.fetchone()
        
        if donor_id:
            self.donor_activity_page(donor_id[0])
        else:
            messagebox.showerror(self.tr('error'), self.tr('invalid_credentials'))

    def donor_register_page(self):
        self.clear_window()
        self._create_header("donor_registration")
        content_frame = self._create_content_frame()
        
        fields = [
            "username", "password", "first_name", "last_name",
            "date_of_birth", "gender", "email", "blood_type", "phone_number"
        ]
        
        self.entries = {}
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=3, fill="x")
            ttk.Label(frame, text=self.tr(field)+":", style="Body.TLabel").pack(side="left", padx=5)
            
            if field == "gender":
                entry = ttk.Combobox(frame, values=[self.tr('male'), self.tr('female')], state="readonly")
            elif field == "blood_type":
                blood_types = ['A', 'B', 'AB', 'A-', 'A+', 'B+', 'B-', 'AB-', 'AB+', 'O', 'O-', 'O+', self.tr('none')]
                entry = ttk.Combobox(frame, values=blood_types, state="readonly")
            elif field == "date_of_birth":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
            self.entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text=self.tr('submit'), command=self.submit_registration, 
                 style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text=self.tr('back'), command=self.donor_login_page, 
                 style="TButton").pack(side="left", padx=5)

    def submit_registration(self):
        data = {k: v.get() for k, v in self.entries.items()}
   

        if not (data["phone_number"].startswith("09") or data["phone_number"].startswith("07")) or len(data["phone_number"]) != 10:
            messagebox.showerror(self.tr('error'), self.tr('invalid_phone'))
            return
        
        try:
            cursor.execute("""
                INSERT INTO Donors (username, password, first_name, last_name, 
                date_of_birth, gender, email, blood_type, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["username"], data["password"], data["first_name"], data["last_name"],
                data["date_of_birth"], data["gender"], data["email"] if data["email"] else None,
                data["blood_type"], data["phone_number"]
            ))
            conn.commit()
            messagebox.showinfo(self.tr('success'), self.tr('registration_success'))
            self.donor_login_page()
        except Exception as e:
            messagebox.showerror(self.tr('error'), str(e))

    def donor_activity_page(self, donor_id):
        self.clear_window()
        self.donor_id = donor_id
        self._create_header("donor_activity")
        content_frame = self._create_content_frame()
        
        buttons = [
            ("make_appointment", self.make_appointment),
            ("view_medical_history", self.view_medical_history),
            ("view_health_status", self.view_health_status),
            ("logout", self.show_welcome_page)
        ]
        
        for text_key, command in buttons:
            ttk.Button(content_frame, text=self.tr(text_key), command=command, 
                     style="TButton").pack(pady=5, fill="x")

    def make_appointment(self):
        window = tk.Toplevel(self.root)
        window.title(self.tr('make_appointment'))
        window.configure(bg=BG_COLOR)
        content_frame = tk.Frame(window, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = ["appointment_date", "appointment_time", "appointment_message"]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=self.tr(field)+":", style="Body.TLabel").pack(side="left", padx=5)
            
            if field == "appointment_date":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
            entries[field] = entry
            
        def submit():
            try:
                appt_date = entries["appointment_date"].get()
                appt_time = entries["appointment_time"].get()
                message = entries["appointment_message"].get()
            
                appt_date = datetime.strptime(entries["appointment_date"].get(), '%Y-%m-%d')
                appt_time = datetime.strptime(entries["appointment_time"].get(), '%H:%M')

                
                if len(message) > 500:
                    messagebox.showerror(self.tr('error'), "Message exceeds 500 characters.")
                    return
                
                cursor.execute("""
                    INSERT INTO Appointments (donor_id, appointment_date, appointment_time, message, status)
                    VALUES (?, ?, ?, ?, 'Pending')
                """, (self.donor_id, appt_date, appt_time, message))
                conn.commit()
                messagebox.showinfo(self.tr('success'), self.tr('appointment_success'))
                window.destroy()
                            
            except ValueError as ve:
                    messagebox.showerror("Input Error", str(ve))
            except pyodbc.Error as e:
                    messagebox.showerror("Database Error", f"Failed to create appointment:\n{str(e)}")
                    conn.rollback()
                    
        ttk.Button(content_frame, text="Submit", command=submit, style="TButton").pack(pady=10, fill="x")

    def view_medical_history(self):
        cursor.execute("""
            SELECT entry_date, hiv_status, syphilis_status, hepatitis_status, sugar_level, outcome_message 
            FROM MedicalHistories WHERE donor_id=?
        """, (self.donor_id,))
        results = cursor.fetchall()
        
        # Process results to format dates and decimals
        processed_results = []
        for row in results:
            new_row = []
            for value in row:
                if isinstance(value, datetime.date):
                    new_value = value.strftime("%Y-%m-%d")  # Format date
                elif isinstance(value, Decimal):
                    new_value = float(value)  # Convert Decimal to float
                else:
                    new_value = value
                new_row.append(new_value)
            processed_results.append(tuple(new_row))
        
        # Create window and Treeview as before
        window = tk.Toplevel(self.root)
        window.title(self.tr('medical_history'))
        
        tree_frame = tk.Frame(window, bg=BG_COLOR)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        columns = ["Date", "hiv_status", "syphilis_status", "hepatitis_status", "sugar_level", "outcome_message"]
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        for col in columns:
            tree.heading(col, text=self.tr(col))
            tree.column(col, width=150, anchor="center", stretch=tk.YES)
         
        for row in processed_results:  # Insert processed results
            tree.insert("", "end", values=row)

    def view_health_status(self):
        cursor.execute("""
            SELECT donation_date, weight, blood_pressure, sugar_level, start_time, end_time 
            FROM HealthStatuses WHERE donor_id=?
        """, (self.donor_id,))
        results = cursor.fetchall()
        
        # Process results to format dates and decimals
        processed_results = []
        for row in results:
            new_row = []
            for value in row:
                if isinstance(value, datetime.date):
                    new_value = value.strftime("%Y-%m-%d")  # Format date
                elif isinstance(value, Decimal):
                    new_value = float(value)  # Convert Decimal to float
                else:
                    new_value = value
                new_row.append(new_value)
            processed_results.append(tuple(new_row))
        
        # Create window and Treeview as before
        window = tk.Toplevel(self.root)
        window.title(self.tr('health_status'))
        
        tree_frame = tk.Frame(window, bg=BG_COLOR)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        columns = ["Date", "weight", "blood_pressure", "sugar_level", "start_time", "end_time"]
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        for col in columns:
            tree.heading(col, text=self.tr(col))
            tree.column(col, width=150, anchor="center", stretch=tk.YES)
        
        for row in processed_results:  # Insert processed results
            tree.insert("", "end", values=row)

    # ================== SUPERVISOR SECTION ==================
    def supervisor_login_page(self):
        self.clear_window()
        self._create_header("supervisor_login")
        content_frame = self._create_content_frame()
        
        fields = ["full_name", "username", "password"]
        self.sup_entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=self.tr(field)+":", style="Body.TLabel").pack(side="left", padx=5)
            entry = ttk.Entry(frame, style="TEntry", show="*" if field == "password" else "")
            entry.pack(side="right", expand=True, fill="x", padx=5)
            self.sup_entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text=self.tr('login'), command=self.supervisor_login, 
                 style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text=self.tr('back'), command=self.show_welcome_page, 
                 style="TButton").pack(side="left", padx=5)

    def supervisor_login(self):
        data = {k: v.get() for k, v in self.sup_entries.items()}
        
        cursor.execute("""
            SELECT supervisor_id FROM Supervisors 
            WHERE full_name=? AND username=? AND password=?
        """, (data["full_name"], data["username"], data["password"]))
        supervisor_id = cursor.fetchone()
        
        if supervisor_id:
            self.supervisor_activity_page(supervisor_id[0])
        else:
            messagebox.showerror(self.tr('error'), self.tr('invalid_credentials'))

    def supervisor_activity_page(self, supervisor_id):
        self.clear_window()
        self.supervisor_id = supervisor_id
        self._create_header("supervisor_activity")
        content_frame = self._create_content_frame()
        
        buttons = [
            ("view_donors", self.view_donors),
            ("send_medical_history", self.send_medical_history),
            ("send_health_status", self.send_health_status),
            ("logout", self.show_welcome_page)
        ]
        
        for text_key, command in buttons:
            ttk.Button(content_frame, text=self.tr(text_key), command=command, 
                     style="TButton").pack(pady=5, fill="x")

    def view_donors(self):
        cursor.execute("SELECT * FROM Donors")
        results = cursor.fetchall()
        
        window = tk.Toplevel(self.root)
        window.title(self.tr('view_donors'))
        
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
            tree.heading(col, text=self.tr(col.lower()))
            tree.column(col, width=100, anchor="center")
        
        for row in results:
            formatted_row = list(row)
            formatted_row[5] = str(formatted_row[5])
            tree.insert("", "end", values=formatted_row)

    def send_medical_history(self):
        window = tk.Toplevel(self.root)
        window.title(self.tr('send_medical_history'))
        content_frame = tk.Frame(window, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            "donor_username", "entry_date", "hiv_status", 
            "syphilis_status", "hepatitis_status", "sugar_level", "outcome_message"
        ]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=3, fill="x")
            ttk.Label(frame, text=self.tr(field)+":", style="Body.TLabel").pack(side="left", padx=5)
            
            if field in ["hiv_status", "syphilis_status", "hepatitis_status"]:
                entry = ttk.Combobox(frame, values=[self.tr('positive'), self.tr('negative')], state="readonly")
            elif field == "entry_date":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
            entries[field] = entry
        
        def submit():
            donor_username = entries["donor_username"].get()
            cursor.execute("SELECT donor_id FROM Donors WHERE username=?", (donor_username,))
            donor_id = cursor.fetchone()
            
            if not donor_id:
                messagebox.showerror(self.tr('error'), self.tr('invalid_donor'))
                return
            
            try:
                cursor.execute("""
                    INSERT INTO MedicalHistories (donor_id, supervisor_id, entry_date, 
                    hiv_status, syphilis_status, hepatitis_status, sugar_level, outcome_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    donor_id[0], self.supervisor_id,
                    entries["entry_date"].get(),
                    entries["hiv_status"].get(),
                    entries["syphilis_status"].get(),
                    entries["hepatitis_status"].get(),
                    entries["sugar_level"].get(),
                    entries["outcome_message"].get()
                ))
                conn.commit()
                messagebox.showinfo(self.tr('success'), self.tr('medical_history_added'))
                window.destroy()
            except Exception as e:
                messagebox.showerror(self.tr('error'), str(e))
        
        ttk.Button(content_frame, text=self.tr('submit'), command=submit, 
                 style="TButton").pack(pady=10, fill="x")

    def send_health_status(self):
        window = tk.Toplevel(self.root)
        window.title(self.tr('send_health_status'))
        content_frame = tk.Frame(window, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            "donor_username", "donation_date", "weight", 
            "blood_pressure", "sugar_level", "start_time", "end_time"
        ]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=3, fill="x")
            ttk.Label(frame, text=self.tr(field)+":", style="Body.TLabel").pack(side="left", padx=5)
            
            if field == "donation_date":
                entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame, style="TEntry")
            
            entry.pack(side="right", expand=True, fill="x", padx=5)
            entries[field] = entry
        
        def submit():
            donor_username = entries["donor_username"].get()
            cursor.execute("SELECT donor_id FROM Donors WHERE username=?", (donor_username,))
            donor_id = cursor.fetchone()
            
            if not donor_id:
                messagebox.showerror(self.tr('error'), self.tr('invalid_donor'))
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
                    entries["donation_date"].get(),
                    entries["weight"].get(),
                    entries["blood_pressure"].get(),
                    entries["sugar_level"].get(),
                    entries["start_time"].get(),
                    entries["end_time"].get()
                ))
                conn.commit()
                messagebox.showinfo(self.tr('success'), self.tr('health_status_added'))
                window.destroy()
            except Exception as e:
                messagebox.showerror(self.tr('error'), str(e))
        
        ttk.Button(content_frame, text=self.tr('submit'), command=submit, 
                 style="TButton").pack(pady=10, fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.minsize(800, 600)
    app = BloodDonationSystem(root)
    root.mainloop()