import tkinter as tk
from tkinter import messagebox
from donor_register_page import user_db

class DonorLoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Login")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Donor Login", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.email_label = tk.Label(root, text="Email", font=("Helvetica", 12))
        self.email_label.pack()
        self.email_entry = tk.Entry(root, font=("Helvetica", 12))
        self.email_entry.pack(pady=10)

        self.password_label = tk.Label(root, text="Password", font=("Helvetica", 12))
        self.password_label.pack()
        self.password_entry = tk.Entry(root, font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(root, text="Login", font=("Helvetica", 12), command=self.login)
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=self.exit_application)
        self.exit_button.pack(pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in user_db and user_db[email] == password:
            messagebox.showinfo("Login Successful", "Logged in successfully!")
            self.root.withdraw()
            # Go to Donor Dashboard or Home page here
        else:
            messagebox.showerror("Login Error", "Invalid email or password")

    def exit_application(self):
        self.root.quit()
