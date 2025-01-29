def doner_wellcome():
    print("\nWelcome to Donor Bank X!")
    print("-------------------------")
    print("1. Register a New Donor")
    print("2. Appointment")
    print("3. View Medical Information")
    print("4. Exit")
    
    options = input("Please choose an option (1, 2, 3, 4): ")
    
    if options == "1":
        register()
    elif options == "2":
        appointment()
    elif options == "3":
        medical_information()
    elif options == "4":
        print("Exiting... Goodbye!")
        return  # Exit the program gracefully
    else:
        print("Invalid choice!")
        doner_wellcome()  # Recursively call the function if input is invalid

def register():
    with open("doner.txt", "a") as file:
        print("Registration Form:")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        date_of_birth = input("Enter your date of birth: ")
        gender = input("Enter your gender (male or female): ")
        blood_type = input("Enter your blood type (A, A+, A-, B, B+, B-, O, O+, O-, AB): ")
        email = input("Enter your email address: ")
        phone = input("Enter your phone number: ")
        address = input("Enter your address: ")
        
        # Save donor information to file
        file.write(f"{first_name} {last_name} {date_of_birth} {gender} {blood_type} {email} {phone} {address}\n")
        print("Thank you for registering!")
        doner_wellcome()
def appointment():
    email = input("Enter your email address: ")
    appointment_found = False
    try:
        with open("doner.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                donor_info = line.strip().split()
                if donor_info[5] == email:  # email is at index 5
                    appointment_found = True
                    print("Appointment Form:")
                    date = input("Enter your appointment date: ")
                    time = input("Enter your appointment time: ")
                    with open("appointments.txt", "a") as appt_file:
                        appt_file.write(f"{email} {date} {time}\n")
                    print("Your appointment has been scheduled!")
                    break
            if not appointment_found:
                print("No donor found with that email!")
    except FileNotFoundError:
        print("The donors' file does not exist yet. Please register first.")

def medical_information():
    # Placeholder function, you can add the logic as per your requirements.
    print("This feature is under development.")

# Call the doner_wellcome function to start the program
doner_wellcome()
