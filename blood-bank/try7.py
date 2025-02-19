import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

# Database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=KALKIDAN;'
    'DATABASE=BloodDonationSystem;'
    'UID=sa;'
    'PWD=kalkidan'
)
cursor = conn.cursor()

# Style configuration
BG_COLOR = "#ffe6e6"  # Light pink background
BUTTON_COLOR = "#cc0000"  # Dark red
BUTTON_TEXT_COLOR = "white"
HEADER_COLOR = "#cc0000"
TEXT_COLOR = "#333333"
ENTRY_BG = "white"

class BloodDonationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donation System")
        self.root.configure(bg=BG_COLOR)
        self.style = ttk.Style()
        self._configure_styles()
        self.show_welcome_page()
        
    def _configure_styles(self):
        self.style.configure("TButton", 
                           foreground=TEXT_COLOR,
                           background=BUTTON_COLOR,
                           font=("Arial", 10, "bold"),
                           padding=10)
        self.style.map("TButton",
                      background=[("active", "#ff3333"), ("disabled", "#cccccc")])
        
        self.style.configure("Header.TLabel",
                            font=("Arial", 18, "bold"),
                            foreground="white",
                            background=HEADER_COLOR,
                            padding=10)
                            
        self.style.configure("Body.TLabel",
                            font=("Arial", 10),
                            background=BG_COLOR,
                            foreground=TEXT_COLOR)
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_welcome_page(self):
        self.clear_window()
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(header_frame, text="Welcome to Blood Donation System", style="Header.TLabel").pack()
        
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        ttk.Button(content_frame, text="Donor", command=self.donor_login_page, style="TButton").pack(pady=10, fill="x")
        ttk.Button(content_frame, text="Supervisor", command=self.supervisor_login_page, style="TButton").pack(pady=10, fill="x")

    # Donor related functions
    def donor_login_page(self):
        self.clear_window()
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text="Donor Login", style="Header.TLabel").pack()
        
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            ("Username", "entry"), 
            ("Password", "entry")
        ]
        
        self.donor_entries = {}
        for field, widget_type in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=field+":", style="Body.TLabel").pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(side="right", expand=True, fill="x")
            self.donor_entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.donor_login, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Register", command=self.donor_register_page, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_welcome_page, style="TButton").pack(side="left", padx=5)

    # ... (Keep all existing database functions the same, only modify GUI components)

    def donor_register_page(self):
        self.clear_window()
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text="Donor Registration", style="Header.TLabel").pack()
        
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            ("Username", "entry"), ("Password", "entry"),
            ("First Name", "entry"), ("Last Name", "entry"),
            ("Date of Birth (YYYY-MM-DD)", "entry"), 
            ("Gender (Male/Female)", "entry"), ("Email", "entry"),
            ("Blood Type", "entry"), ("Phone Number", "entry")
        ]
        
        self.entries = {}
        for field, widget_type in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=field+":", style="Body.TLabel").pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(side="right", expand=True, fill="x")
            self.entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Submit", command=self.submit_registration, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.donor_login_page, style="TButton").pack(side="left", padx=5)

    # ... (Continue modifying all GUI components similarly)

    def supervisor_login_page(self):
        self.clear_window()
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text="Supervisor Login", style="Header.TLabel").pack()
        
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(padx=20, pady=20)
        
        fields = [
            ("Full Name", "entry"), 
            ("Username", "entry"),
            ("Password", "entry")
        ]
        
        self.sup_entries = {}
        for field, widget_type in fields:
            frame = tk.Frame(content_frame, bg=BG_COLOR)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=field+":", style="Body.TLabel").pack(side="left")
            entry = ttk.Entry(frame, show="*" if "Password" in field else "")
            entry.pack(side="right", expand=True, fill="x")
            self.sup_entries[field] = entry
        
        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.supervisor_login, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_welcome_page, style="TButton").pack(side="left", padx=5)

    # ... (Modify remaining pages similarly with consistent styling)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    app = BloodDonationSystem(root)
    root.mainloop()