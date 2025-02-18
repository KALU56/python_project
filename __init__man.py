

import supervise
import doners_i

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
            doners_i.register()
        elif option == "2":
            doners_i.appointment()
        elif option == "3":
            doners_i.check_appointment_status()
        elif option == "4":
            doners_i.notify_donor()
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
            supervise.view_donors()  # Corrected function call
        elif option == "2":
            supervise.approve_appointments()# Corrected function call
        elif option == "3":
            supervise.record_medical_history()
        elif option == "4":
            supervise.record_health_state()   
        elif option == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")



def BloodBank():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1.Donor")
        print("2.superviser")
       
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