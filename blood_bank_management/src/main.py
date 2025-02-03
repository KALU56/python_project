from src.gui.doner_gui import donor_welcome
from src.gui.supervisor_gui import supervisor_welcome

def donor_welcome():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1. Register a New Donor")
        print("2. Schedule an Appointment")
        print("3. See Appointment Approval Status")
        print("4. View Medical Information")
        print("5. Exit")

        option = input("Please choose an option (1, 2, 3, 4, 5): ").strip()

        if option == "1":
            doner_gui.register()
        elif option == "2":
            doner_gui.appointment()
        elif option == "3":
            doner_gui.check_appointment_status()
        elif option == "4":
            doner_gui.notify_donor()
        elif option == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")




def supervisor_welcome():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1. all doner see")
        print("2. approved the appointment")
        print("3. send Medical Information")
        print("4. record health state")
        print("5. Exit")
        
        option = input("Please choose an option (1, 2, 3, 4): ").strip()
        
        if option == "1":
            supervisor_gui.view_donors()  # Corrected function call
        elif option == "2":
            supervisor_gui.approve_appointments()# Corrected function call
        elif option == "3":
            supervisor_gui.record_medical_history()
        elif option == "4":
            supervisor_gui.record_health_state()   
        elif option == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

def BloodBank():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1. Donor")
        print("2. Supervisor")
        print("3. Exit")

        option = input("Please choose an option (1, 2, 3): ").strip()

        if option == "1":
            donor_welcome()
        elif option == "2":
            supervisor_welcome()
        elif option == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    BloodBank()