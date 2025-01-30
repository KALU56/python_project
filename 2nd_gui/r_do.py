import tkinter as tk
from tkinter import messagebox
import uuid
from datetime import datetime
import re

def validate_date_of_birth(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.today() - birth_date).days // 365
        return age >= 18
    except ValueError:
        return False

def validate_phone_number(phone_number):
    return re.match(r"^(09|07)\d{8}$", phone_number) is not None

def register_donor():
    # Create a new window for registration
    register_window = tk.Toplevel()
    register_window.title("Register Donor")
    register_window.geometry("400x600")
    
    # Labels and entries for donor details
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

    # Submit button to handle registration
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

        if not validate_date_of_birth(date_of_birth):
            messagebox.showerror("Error", "Invalid date of birth. You must be 18 or older and use YYYY-MM-DD format.")
            return
        
        if not validate_phone_number(phone_number):
            messagebox.showerror("Error", "Invalid phone number. It must start with 09 or 07 and be 10 digits long.")
            return
        
        if not email.endswith("@gmail.com"):
            messagebox.showerror("Error", "Invalid email. Please use a Gmail address ending with @gmail.com.")
            return

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

    # Register button to submit the form
    tk.Button(register_window, text="Register", command=submit_registration).pack()

