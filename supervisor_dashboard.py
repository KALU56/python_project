import tkinter as tk

class SupervisorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Supervisor Dashboard")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Welcome to Supervisor Dashboard", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.dashboard_label = tk.Label(root, text="This is your dashboard", font=("Helvetica", 12))
        self.dashboard_label.pack(pady=20)

        self.logout_button = tk.Button(root, text="Logout", font=("Helvetica", 12), command=self.logout)
        self.logout_button.pack(pady=10)

    def logout(self):
        self.root.quit()
