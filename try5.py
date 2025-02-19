import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

# Database connection
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=KALKIDAN;'
    'DATABASE=BloodBank;'
    'UID=sa;'
    'PWD=kalkidan;'
)
cursor = conn.cursor()

def welcome():
    root.title("Welcome Page")
    root.geometry("400x300")

    label = tk.Label(root, text="Welcome to the Blood Bank Management System", font=("Helvetica", 14))
    label.pack(pady=20)

    donor_button = tk.Button(root, text="Donor", font=("Helvetica", 12), command=donor)
    donor_button.pack(pady=10)

    supervisor_button = tk.Button(root, text="Supervisor", font=("Helvetica", 12), command=supervisor)
    supervisor_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=root.quit)
    exit_button.pack(pady=10)

def donor():
    donor_window = tk.Toplevel(root)
    donor_window.title("Donor Page")
    donor_window.geometry("400x300")

    label = tk.Label(donor_window, text="Donor Page", font=("Helvetica", 14))
    label.pack(pady=20)

    register_button = tk.Button(donor_window, text="Register", font=("Helvetica", 12), command=register_donor)
    register_button.pack(pady=10)

    login_button = tk.Button(donor_window, text="Login", font=("Helvetica", 12), command=login_donor)
    login_button.pack(pady=10)

def supervisor():
    supervisor_window = tk.Toplevel(root)
    supervisor_window.title("Supervisor Page")
    supervisor_window.geometry("400x300")

    label = tk.Label(supervisor_window, text="Supervisor Page", font=("Helvetica", 14))
    label.pack(pady=20)

    donor_view_button = tk.Button(supervisor_window, text="View Donors", font=("Helvetica", 12))
    donor_view_button.pack(pady=10)

    send_medical_history_button = tk.Button(supervisor_window, text="Send Medical History", font=("Helvetica", 12))
    send_medical_history_button.pack(pady=10)

def register_donor():
    username = entry_username.get()
    password = entry_password.get()
    first_name = entry_firstname.get()
    last_name = entry_lastname.get()
    date_of_birth = entry_dob.get()
    gender = gender_var.get()
    email = entry_email.get()
    blood_type = blood_type_var.get()
    phone_number = entry_phone.get()
    
    try:
        cursor.execute("INSERT INTO Donors (username, password_hash, first_name, last_name, date_of_birth, gender, email, blood_type, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (username, password, first_name, last_name, date_of_birth, gender, email, blood_type, phone_number))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def login_donor():
    username = entry_username.get()
    password = entry_password.get()
    cursor.execute("SELECT * FROM Donors WHERE username = ? AND password_hash = ?", (username, password))
    donor = cursor.fetchone()
    if donor:
        messagebox.showinfo("Success", "Login successful!")
        open_donor_dashboard()
    else:
        messagebox.showerror("Error", "Invalid credentials!")

def open_donor_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("Donor Dashboard")
    dashboard.geometry("400x300")
    
    btn_appointment = tk.Button(dashboard, text="Schedule Appointment")
    btn_appointment.pack()
    
    btn_medical_history = tk.Button(dashboard, text="View Medical History")
    btn_medical_history.pack()
    
    btn_health_status = tk.Button(dashboard, text="View Health Status")
    btn_health_status.pack()

root = tk.Tk()
root.title("Blood Bank System")
root.geometry("400x400")

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

lbl_username = tk.Label(scrollable_frame, text="Username")
lbl_username.pack()
entry_username = tk.Entry(scrollable_frame)
entry_username.pack()

lbl_password = tk.Label(scrollable_frame, text="Password")
lbl_password.pack()
entry_password = tk.Entry(scrollable_frame, show='*')
entry_password.pack()

lbl_firstname = tk.Label(scrollable_frame, text="First Name")
lbl_firstname.pack()
entry_firstname = tk.Entry(scrollable_frame)
entry_firstname.pack()

lbl_lastname = tk.Label(scrollable_frame, text="Last Name")
lbl_lastname.pack()
entry_lastname = tk.Entry(scrollable_frame)
entry_lastname.pack()

lbl_dob = tk.Label(scrollable_frame, text="Date of Birth (YYYY-MM-DD)")
lbl_dob.pack()
entry_dob = tk.Entry(scrollable_frame)
entry_dob.pack()

gender_var = tk.StringVar(value="Male")
tk.Label(scrollable_frame, text="Gender").pack()
tk.Radiobutton(scrollable_frame, text="Male", variable=gender_var, value="Male").pack()
tk.Radiobutton(scrollable_frame, text="Female", variable=gender_var, value="Female").pack()

lbl_email = tk.Label(scrollable_frame, text="Email (Optional)")
lbl_email.pack()
entry_email = tk.Entry(scrollable_frame)
entry_email.pack()

blood_type_var = tk.StringVar(value="A")
tk.Label(scrollable_frame, text="Blood Type").pack()
tk.OptionMenu(scrollable_frame, blood_type_var, "A", "B", "AB", "A-", "A+", "B+", "B-", "None").pack()

lbl_phone = tk.Label(scrollable_frame, text="Phone Number")
lbl_phone.pack()
entry_phone = tk.Entry(scrollable_frame)
entry_phone.pack()

btn_register = tk.Button(scrollable_frame, text="Register", command=register_donor)
btn_register.pack()

btn_login = tk.Button(scrollable_frame, text="Login", command=login_donor)
btn_login.pack()

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

welcome()
root.mainloop()
