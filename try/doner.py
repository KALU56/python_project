import uuid
import re
from datetime import datetime
import try.register as register  # Importing register module
import try.appointment as appointment  # Importing appointment module

def donor_welcome():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1. Register a New Donor")
        print("2. Schedule an Appointment")
        print("3. View Medical Information")
        print("4. Exit")
        
        option = input("Please choose an option (1, 2, 3, 4): ").strip()
        
        if option == "1":
            register.register()
        elif option == "2":
            appointment.appointment()
        elif option == "3":
            print("Medical Information feature is under development.")
        elif option == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    donor_welcome()
