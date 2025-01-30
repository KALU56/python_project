import tkinter as tk
from tkinter import messagebox
import uuid
from datetime import datetime
import re
import register_gui  # Ensure this file exists and contains the register_donor function
import appointment_gui  # Ensure this file exists and contains the appointment function

# Validation Functions
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

def validate_date_of_birth(dob):
    """Validate donor's date of birth (must be 18 years or older)."""
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.today() - birth_date).days // 365
        return age >= 18
    except ValueError:
        return False

def validate_phone_number(phone_number):
    """Validate phone number format."""
    return re.match(r"^(09|07)\d{8}$", phone_number) is not None

# Donor Registration Function
def register_donor():
    """Function to open donor registration window."""
    register_gui.register_donor()  # Open donor registration window

# Appointment Scheduling Function
def schedule_appointment():
    """Function to open appointment scheduling window."""
    appointment_gui.appointment()  # Open appointment scheduling window

# Function to View Medical Information (Under Development)
def view_medical_info():
    messagebox.showinfo("Medical Information", "This feature is under development.")

# Exit Function
def exit_app(root):
    root.quit()

# Main Application Window
def create_main_window():
    """Creates and manages the main window with buttons for navigation."""
    root = tk.Tk()
    root.title("Donor Bank X")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    # Title Label
    title_label = tk.Label(root, text="Welcome to Donor Bank X!", font=("Arial", 14, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Buttons for Main Actions
    register_button = tk.Button(root, text="Register a New Donor", command=register_donor, width=30, height=2, bg="#4CAF50", fg="white")
    register_button.pack(pady=5)

    appointment_button = tk.Button(root, text="Schedule an Appointment", command=schedule_appointment, width=30, height=2, bg="#2196F3", fg="white")
    appointment_button.pack(pady=5)

    medical_button = tk.Button(root, text="View Medical Information", command=view_medical_info, width=30, height=2, bg="#FF9800", fg="white")
    medical_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=lambda: exit_app(root), width=30, height=2, bg="#f44336", fg="white")
    exit_button.pack(pady=5)

    # Run the main window loop
    root.mainloop()

# Registration Window (Updated with validation)
def register_donor_window():
    """Create a donor registration window."""
    register_window = tk.Toplevel()
    register_window.title("Register Donor")
    register_window.geometry("400x600")

    # Labels and Entries for Donor Details
    tk.Label(register_window, text="First Name:").pack()
    first_name_entry = tk.Entry(register_window)
    first_name_entry.pack()

    tk.Label(register_window, text="Last Name:").pack()
    last_name_entry = tk.Entry(register_window)
    last_name_entry.pack()

    tk.Label(register_window, text="Date of Birth (YYYY-MM-DD):").pack()
    dob_entry = tk.Entry(register_window)
    dob_entry.pack()

    tk.Label(register_window, text="Gender:").pack()
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(register_window, text="Male", variable=gender_var, value="Male").pack()
    tk.Radiobutton(register_window, text="Female", variable=gender_var, value="Female").pack()

    tk.Label(register_window, text="Blood Type:").pack()
    blood_type_var = tk.StringVar(value="A")
    tk.OptionMenu(register_window, blood_type_var, "A", "A+", "A-", "B", "B+", "B-", "O", "O+", "O-", "AB", "I DON'T KNOW").pack()

    tk.Label(register_window, text="Email:").pack()
    email_entry = tk.Entry(register_window)
    email_entry.pack()

    tk.Label(register_window, text="Phone Number:").pack()
    phone_entry = tk.Entry(register_window)
    phone_entry.pack()

    tk.Label(register_window, text="Phone Type:").pack()
    phone_type_var = tk.StringVar(value="Mobile")
    tk.OptionMenu(register_window, phone_type_var, "Home", "Mobile", "Work").pack()

    tk.Label(register_window, text="City:").pack()
    city_entry = tk.Entry(register_window)
    city_entry.pack()

    tk.Label(register_window, text="Region:").pack()
    region_entry = tk.Entry(register_window)
    region_entry.pack()

    tk.Label(register_window, text="Wereda:").pack()
    wereda_entry = tk.Entry(register_window)
    wereda_entry.pack()

    tk.Label(register_window, text="Subcity:").pack()
    subcity_entry = tk.Entry(register_window)
    subcity_entry.pack()

    # Submit Registration Function
    def submit_registration():
        donor_id = str(uuid.uuid4())
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        date_of_birth = dob_entry.get()
        gender = gender_var.get()
        blood_type = blood_type_var.get()
        email = email_entry.get()
        phone_number = phone_entry.get()
        phone_type = phone_type_var.get()
        city = city_entry.get()
        region = region_entry.get()
        wereda = wereda_entry.get()
        subcity = subcity_entry.get()

        # Validation of input fields
        if not validate_date_of_birth(date_of_birth):
            messagebox.showerror("Error", "You must be 18 or older.")
            return
        
        if not validate_phone_number(phone_number):
            messagebox.showerror("Error", "Invalid phone number.")
            return
        
        if not email.endswith("@gmail.com"):
            messagebox.showerror("Error", "Invalid email. Use a Gmail address.")
            return

        # Save the registration details in a file
        with open("donor_registration.txt", "a") as file:
            file.write(f"DonorID: {donor_id}\n")
            file.write(f"FirstName: {first_name}\n")
            file.write(f"LastName: {last_name}\n")
            file.write(f"DateOfBirth: {date_of_birth}\n")
            file.write(f"Gender: {gender}\n")
            file.write(f"BloodType: {blood_type}\n")
            file.write(f"Email: {email}\n")
            file.write(f"PhoneNumber: {phone_number}\n")
            file.write(f"PhoneType: {phone_type}\n")
            file.write(f"City: {city}\n")
            file.write(f"Region: {region}\n")
            file.write(f"Wereda: {wereda}\n")
            file.write(f"Subcity: {subcity}\n")
            file.write("----------------------------------------\n")

        messagebox.showinfo("Success", "Donor registration successful!")
        register_window.quit()

    # Register button
    tk.Button(register_window, text="Register", command=submit_registration).pack()

# Run the main window
if __name__ == "__main__":
    create_main_window()
