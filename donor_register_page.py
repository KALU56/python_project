import tkinter as tk
from tkinter import messagebox
from donor_login_page import DonorLoginPage

# Using a simple dictionary to store the credentials temporarily
user_db = {}

class DonorRegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Register")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Donor Register", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.email_label = tk.Label(root, text="Email", font=("Helvetica", 12))
        self.email_label.pack()
        self.email_entry = tk.Entry(root, font=("Helvetica", 12))
        self.email_entry.pack(pady=10)

        self.password_label = tk.Label(root, text="Password", font=("Helvetica", 12))
        self.password_label.pack()
        self.password_entry = tk.Entry(root, font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=10)

        self.register_button = tk.Button(root, text="Register", font=("Helvetica", 12), command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(root, text="Back", font=("Helvetica", 12), command=self.go_back)
        self.back_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=self.exit_application)
        self.exit_button.pack(pady=10)

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:  # Simplified validation
            if email in user_db:
                messagebox.showwarning("Registration Error", "Email already registered!")
            else:
                user_db[email] = password
                messagebox.showinfo("Registration Successful", "You have successfully registered!")
                self.root.withdraw()
                donor_login = DonorLoginPage(tk.Toplevel(self.root))  # Navigate to Donor Login page
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    def go_back(self):
        self.root.withdraw()
        welcome_page = WelcomePage(tk.Toplevel(self.root))  # Navigate back to Welcome page

    def exit_application(self):
        self.root.quit()
