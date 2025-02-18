import tkinter as tk
from tkinter import messagebox
from donor_register_page import user_db

class DonorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Dashboard")
        self.root.geometry("400x400")

        tk.Label(root, text="Donor Dashboard", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(root, text="Put Information", font=("Helvetica", 12), command=self.put_information).pack(pady=10)
        tk.Button(root, text="Appointment", font=("Helvetica", 12), command=self.appointment).pack(pady=10)
        tk.Button(root, text="See Appointment Approval Status", font=("Helvetica", 12), command=self.see_approval_status).pack(pady=10)
        tk.Button(root, text="Back", font=("Helvetica", 12), command=self.go_back).pack(pady=10)
        tk.Button(root, text="Exit", font=("Helvetica", 12), command=self.exit_application).pack(pady=10)

    def put_information(self):
        messagebox.showinfo("Information", "Put Information page")

    def appointment(self):
        messagebox.showinfo("Appointment", "Appointment page")

    def see_approval_status(self):
        messagebox.showinfo("Status", "Appointment Approval Status page")

    def go_back(self):
        self.root.destroy()

    def exit_application(self):
        self.root.quit()
