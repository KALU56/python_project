import tkinter as tk
from donor_register_page import DonorRegisterPage  # Import DonorRegisterPage here
from donor_login_page import DonorLoginPage  # Import DonorLoginPage here

class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome Page")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Welcome to the Blood Bank Management System", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.donor_button = tk.Button(root, text="Donor", font=("Helvetica", 12), command=self.go_to_donor)
        self.donor_button.pack(pady=10)

        self.supervisor_button = tk.Button(root, text="Supervisor", font=("Helvetica", 12), command=self.go_to_supervisor)
        self.supervisor_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=self.root.quit)
        self.exit_button.pack(pady=10)

    def go_to_donor(self):
        self.root.withdraw()
        donor_register_page = DonorRegisterPage(tk.Toplevel(self.root))  # Open Donor Register Page

    def go_to_supervisor(self):
        self.root.withdraw()
        supervisor_page = SupervisorPage(tk.Toplevel(self.root))

if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomePage(root)
    root.mainloop()
