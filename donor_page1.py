import tkinter as tk

class DonorPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Donor Page")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Welcome to the Donor Page", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.back_button = tk.Button(root, text="Back", font=("Helvetica", 12), command=self.go_back)
        self.back_button.pack(pady=10)

    def go_back(self):
        from donor_login_page import DonorLoginPage  # Import here to avoid circular imports
        self.root.withdraw()
        donor_login_page = DonorLoginPage(tk.Toplevel(self.root))
