import tkinter as tk
from tkinter import messagebox
from supervisor_dashboard import SupervisorDashboard

class SupervisorPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Supervisor Login")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Supervisor Login", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.username_label = tk.Label(root, text="Username", font=("Helvetica", 12))
        self.username_label.pack()
        self.username_entry = tk.Entry(root, font=("Helvetica", 12))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(root, text="Password", font=("Helvetica", 12))
        self.password_label.pack()
        self.password_entry = tk.Entry(root, font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(root, text="Login", font=("Helvetica", 12), command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "sup" and password == "1234":
            self.root.withdraw()
            supervisor_dashboard = SupervisorDashboard(tk.Toplevel(self.root))
        else:
            messagebox.showerror("Login Error", "Invalid username or password")
