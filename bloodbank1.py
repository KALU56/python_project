donors_list = []  # Global list to store donor information

def welcome_message():
    print("Welcome to the Blood Bank System!")
    print("Please select your role:")

    print("1. Donor")
    print("2. Supervisor")

    role = input("Enter the number corresponding to your role: ")

    if role == '1':
        print("Welcome, Blood Bank Management!")
       
    elif role == '2':
        print("Welcome, Donor!")
        doner()
    elif role == '3':
        print("Welcome, Supervisor!")
        supervisor()
    else:
        print("Invalid input. Please enter 1, 2, or 3.")

def doner():
    print("Welcome to the donor page!")
    print("Please select what you want to do:")
    print("1. Registration")
    print("2. Appointment")
    print("3. View Medical Information")
    
    choice = input("Enter the number corresponding to your choice: ")
    
    if choice == '1':
        registration()
    elif choice == '2':
        appointment()
    elif choice == '3':
        medical_info()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")

def registration():
    # Collecting donor details and adding them to the list
    doner_firstname = input("Enter your first name: ")
    doner_lastname = input("Enter your last name: ")
    date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
    email = input("Enter your email: ")
    blood_type = input("Enter your blood type: ")
    
    donor = {
        'first_name': doner_firstname,
        'last_name': doner_lastname,
        'dob': date_of_birth,
        'email': email,
        'blood_type': blood_type
    }
    donors_list.append(donor)  # Add the donor to the list
    print(f"Thank you, {doner_firstname} {doner_lastname}, for registering as a donor!")

def appointment():
    # Collecting appointment details
    app_date = input("Enter your appointment date (YYYY-MM-DD): ")
    app_time = input("Enter your appointment time (HH:MM): ")
    
    appointment_details = {
        'date': app_date,
        'time': app_time
    }
    print("Appointment successfully scheduled.")
    return appointment_details

def medical_info():
    print("Medical information page is under development.")
    # You can implement medical history fetching here
    return "Medical history not available."

def supervisor():
    print("Welcome to the supervisor page!")
    print("Please select what you want to do:")
    print("1. Supervise")
    print("2. Approve Donor Registration")
    print("3. Send Medical Information")
    
    choice = input("Enter the number corresponding to your choice: ")
    
    if choice == '1':
        supervise()
    elif choice == '2':
        approval()
    elif choice == '3':
        send_medical_info()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")

def supervise():
    print("Supervising all donors and appointments.")
    # Implement the logic to view all donors and appointments.
    for donor in donors_list:
        print(f"Donor: {donor['first_name']} {donor['last_name']}, Blood Type: {donor['blood_type']}")
    return donors_list

def approval():
    print("Approving or rejecting donor requests.")
    if not donors_list:
        print("No donors to approve.")
        return
    donor_index = int(input(f"Select a donor to approve (1-{len(donors_list)}): ")) - 1
    if 0 <= donor_index < len(donors_list):
        print(f"Approving donor {donors_list[donor_index]['first_name']} {donors_list[donor_index]['last_name']}.")
        # Additional logic for approval here (e.g., sending email).
    else:
        print("Invalid donor selection.")

def send_medical_info():
    print("Sending medical information.")
    # Implement email or notification logic here.
    print("Medical information sent to the relevant authorities.")

if __name__ == "__main__":
    welcome_message()
