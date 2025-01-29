import uuid
import re
from datetime import datetime

def validate_date_of_birth(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.today() - birth_date).days // 365
        return age >= 18
    except ValueError:
        return False

def validate_phone_number(phone_number):
    return re.match(r"^(09|07)\d{8}$", phone_number) is not None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def register():
    with open("donor_registration.txt", "a") as file:
        print("Registration Form:")
        donor_id = str(uuid.uuid4())  # Generate a unique DonorID
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        
        while True:
            date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
            if validate_date_of_birth(date_of_birth):
                break
            print("Invalid date of birth. You must be 18 or older and use the format YYYY-MM-DD.")
        
        while True:
            gender = input("Enter your gender (Male/Female): ").strip().capitalize()
            if gender in ["Male", "Female"]:
                break
            print("Invalid gender. Please enter 'Male' or 'Female'.")
        
        while True:
            blood_type = input("Enter your blood type (A, A+, A-, B, B+, B-, O, O+, O-, AB, or I don't know): ").strip().upper()
            if blood_type in ["A", "A+", "A-", "B", "B+", "B-", "O", "O+", "O-", "AB", "I DON'T KNOW"]:
                break
            print("Invalid blood type. Please enter a valid option.")
        
        while True:
            email = input("Enter your email address: ").strip()
            if email.endswith("@gmail.com"):
                break
            print("Invalid email. Please use a Gmail address ending with @gmail.com.")
        
        # Phone details
        phone_ids = []
        while True:
            phone_id = str(uuid.uuid4())  # Unique identifier for phone record
            while True:
                phone_number = input("Enter your phone number (must start with 09 or 07 and be 10 digits long): ")
                if validate_phone_number(phone_number):
                    break
                print("Invalid phone number. It must start with 09 or 07 and be exactly 10 digits.")
            phone_type = input("Enter phone type (Home, Mobile, Work): ")
            phone_ids.append((phone_id, phone_number, phone_type))
            more = input("Do you want to add another phone number? (yes/no): ").strip().lower()
            if more != "yes":
                break
        
        # Address details
        address_id = str(uuid.uuid4())  # Unique identifier for address record
        city = input("Enter your city: ")
        region = input("Enter your region: ")
        wereda = input("Enter your wereda: ")
        subcity = input("Enter your subcity: ")
        
        # Save donor information to file
        file.write(f"DonorID: {donor_id}\n")
        file.write(f"FirstName: {first_name}\n")
        file.write(f"LastName: {last_name}\n")
        file.write(f"DateOfBirth: {date_of_birth}\n")
        file.write(f"Gender: {gender}\n")
        file.write(f"BloodType: {blood_type}\n")
        file.write(f"Email: {email}\n")
        
        for phone_id, phone_number, phone_type in phone_ids:
            file.write(f"DonorPhoneID: {phone_id}\n")
            file.write(f"PhoneNumber: {phone_number}\n")
            file.write(f"PhoneType: {phone_type}\n")
        
        file.write(f"DonorAddressID: {address_id}\n")
        file.write(f"City: {city}\n")
        file.write(f"Region: {region}\n")
        file.write(f"Wereda: {wereda}\n")
        file.write(f"Subcity: {subcity}\n")
        file.write("----------------------------------------\n")
        
        print("Thank you for registering!")

def find_donor_by_email(email):
    """Search donor_registration.txt for a donor by email and return DonorID."""
    try:
        with open("donor_registration.txt", "r") as file:
            donor_id = None
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("Email:") and lines[i].strip().split()[1] == email:
                    # Extract DonorID
                    for j in range(max(0, i - 10), i):
                        if lines[j].startswith("DonorID:"):
                            donor_id = lines[j].strip().split()[1]
                            return donor_id
        return None
    except FileNotFoundError:
        print("Error: Donor registration file not found.")
        return None

def appointment():
    email = input("Enter your email address: ").strip()

    if not validate_email(email):
        print("Invalid email format. Please enter a valid email address.")
        return

    donor_id = find_donor_by_email(email)
    if not donor_id:
        print("No donor found with this email. Please register first.")
        register()  # Call register if donor is not found
        donor_id = find_donor_by_email(email)  # Try fetching donor ID again
        if not donor_id:
            print("Registration failed. Cannot proceed with appointment.")
            return

    appointment_id = str(uuid.uuid4())
    supervisor_id = str(uuid.uuid4())

    while True:
        appointment_date = input("Enter your appointment date (YYYY-MM-DD): ").strip()
        if validate_date(appointment_date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    while True:
        appointment_time = input("Enter your appointment time (HH:MM): ").strip()
        if validate_time(appointment_time):
            break
        print("Invalid time format. Please use HH:MM.")

    appointment_status = "Scheduled"

    try:
        with open("appointments.txt", "a") as appt_file:
            appt_file.write(f"AppointmentID: {appointment_id}\n")
            appt_file.write(f"DonorID: {donor_id}\n")
            appt_file.write(f"SupervisorID: {supervisor_id}\n")
            appt_file.write(f"AppointmentDate: {appointment_date}\n")
            appt_file.write(f"AppointmentTime: {appointment_time}\n")
            appt_file.write(f"AppointmentStatus: {appointment_status}\n")
            appt_file.write("----------------------------------------\n")

        print("Your appointment has been scheduled successfully!")

    except Exception as e:
        print(f"Error saving appointment: {e}")
def see_approval():
    email = input("Enter your email address to check the approval status: ").strip()

    # Validate email
    if not validate_email(email):
        print("Invalid email format. Please enter a valid email address.")
        return

    # Find the donor ID using email
    donor_id = find_donor_by_email(email)
    if not donor_id:
        print("No donor found with this email. Please register first.")
        return

    # Check approved appointments from approve.txt
    print("\nApproved Appointments:")
    found_approved = False
    try:
        with open("approve.txt", "r") as approve_file:
            lines = approve_file.readlines()
            for i in range(0, len(lines), 7):  # 7 lines per appointment
                appointment = {lines[i].split(":")[0].strip(): lines[i].split(":")[1].strip(),
                               lines[i + 1].split(":")[0].strip(): lines[i + 1].split(":")[1].strip(),
                               lines[i + 2].split(":")[0].strip(): lines[i + 2].split(":")[1].strip(),
                               lines[i + 3].split(":")[0].strip(): lines[i + 3].split(":")[1].strip(),
                               lines[i + 4].split(":")[0].strip(): lines[i + 4].split(":")[1].strip(),
                               lines[i + 5].split(":")[0].strip(): lines[i + 5].split(":")[1].strip()}

                if appointment["DonorID"] == donor_id:
                    print(f"Appointment ID: {appointment['AppointmentID']}")
                    print(f"   Supervisor ID: {appointment['SupervisorID']}")
                    print(f"   Date: {appointment['AppointmentDate']}")
                    print(f"   Time: {appointment['AppointmentTime']}")
                    print(f"   Status: {appointment['AppointmentStatus']}")
                    print("----------------------------------------")
                    found_approved = True

        if not found_approved:
            print("No approved appointments found for this donor.")

    except FileNotFoundError:
        print("Error: Approved appointments file not found.")

    # Check unapproved appointments from unapprove.txt
    print("\nUnapproved Appointments:")
    found_unapproved = False
    try:
        with open("unapprove.txt", "r") as unapprove_file:
            lines = unapprove_file.readlines()
            for i in range(0, len(lines), 7):  # 7 lines per appointment
                appointment = {lines[i].split(":")[0].strip(): lines[i].split(":")[1].strip(),
                               lines[i + 1].split(":")[0].strip(): lines[i + 1].split(":")[1].strip(),
                               lines[i + 2].split(":")[0].strip(): lines[i + 2].split(":")[1].strip(),
                               lines[i + 3].split(":")[0].strip(): lines[i + 3].split(":")[1].strip(),
                               lines[i + 4].split(":")[0].strip(): lines[i + 4].split(":")[1].strip(),
                               lines[i + 5].split(":")[0].strip(): lines[i + 5].split(":")[1].strip()}

                if appointment["DonorID"] == donor_id:
                    print(f"Appointment ID: {appointment['AppointmentID']}")
                    print(f"   Supervisor ID: {appointment['SupervisorID']}")
                    print(f"   Date: {appointment['AppointmentDate']}")
                    print(f"   Time: {appointment['AppointmentTime']}")
                    print(f"   Status: {appointment['AppointmentStatus']}")
                    print("----------------------------------------")
                    found_unapproved = True

        if not found_unapproved:
            print("No unapproved appointments found for this donor.")

    except FileNotFoundError:
        print("Error: Unapproved appointments file not found.")


def view_donors():
    try:
        donors_list = []
        with open("donor_registration.txt", "r") as file:
            lines = file.readlines()

            donor_data = {}
            for line in lines:
                line = line.strip()
                if line.startswith("DonorID:"):
                    if donor_data:  # If donor_data is not empty, add the previous donor data to the list
                        donors_list.append(donor_data)
                    donor_data = {"DonorID": line.split(":")[1].strip()}  # Start new donor
                elif line.startswith("FirstName:"):
                    donor_data["FirstName"] = line.split(":")[1].strip()
                elif line.startswith("LastName:"):
                    donor_data["LastName"] = line.split(":")[1].strip()
                elif line.startswith("BloodType:"):
                    donor_data["BloodType"] = line.split(":")[1].strip()
                elif line.startswith("DateOfBirth:"):
                    donor_data["DateOfBirth"] = line.split(":")[1].strip()
                # Add more fields as needed
            if donor_data:  # Add the last donor after finishing reading the file
                donors_list.append(donor_data)

        # Now you can access donors using indexes
        if donors_list:
            for donor in donors_list:
                print(f"Donor ID: {donor['DonorID']}, Name: {donor['FirstName']} {donor['LastName']}, Blood Type: {donor['BloodType']}, Date of Birth: {donor['DateOfBirth']}")
        else:
            print("No donor data found.")
    except FileNotFoundError:
        print("The donors' file does not exist yet. Please register first.")

# Example of accessing a donor by index
def view_single_donor(index):
    try:
        donors_list = []
        with open("donor_registration.txt", "r") as file:
            lines = file.readlines()

            donor_data = {}
            for line in lines:
                line = line.strip()
                if line.startswith("DonorID:"):
                    if donor_data:  # If donor_data is not empty, add the previous donor data to the list
                        donors_list.append(donor_data)
                    donor_data = {"DonorID": line.split(":")[1].strip()}  # Start new donor
                elif line.startswith("FirstName:"):
                    donor_data["FirstName"] = line.split(":")[1].strip()
                elif line.startswith("LastName:"):
                    donor_data["LastName"] = line.split(":")[1].strip()
                elif line.startswith("BloodType:"):
                    donor_data["BloodType"] = line.split(":")[1].strip()
                elif line.startswith("DateOfBirth:"):
                    donor_data["DateOfBirth"] = line.split(":")[1].strip()
            if donor_data:  # Add the last donor after finishing reading the file
                donors_list.append(donor_data)

        # Now you can access donors by index
        if 0 <= index < len(donors_list):
            donor = donors_list[index]
            print(f"Donor ID: {donor['DonorID']}, Name: {donor['FirstName']} {donor['LastName']}, Blood Type: {donor['BloodType']}, Date of Birth: {donor['DateOfBirth']}")
        else:
            print("Invalid index. Please select a valid donor index.")
    except FileNotFoundError:
        print("The donors' file does not exist yet. Please register first.")
def approval():
    try:
        appointments_list = []
        with open("appointments.txt", "r") as file:
            lines = file.readlines()

            appointment_data = {}
            for line in lines:
                line = line.strip()
                if line.startswith("AppointmentID:"):
                    if appointment_data:  # If appointment_data is not empty, add the previous appointment data to the list
                        appointments_list.append(appointment_data)
                    appointment_data = {"AppointmentID": line.split(":")[1].strip()}  # Start new appointment
                elif line.startswith("DonorID:"):
                    appointment_data["DonorID"] = line.split(":")[1].strip()
                elif line.startswith("SupervisorID:"):
                    appointment_data["SupervisorID"] = line.split(":")[1].strip()
                elif line.startswith("AppointmentDate:"):
                    appointment_data["AppointmentDate"] = line.split(":")[1].strip()
                elif line.startswith("AppointmentTime:"):
                    appointment_data["AppointmentTime"] = line.split(":")[1].strip()
                elif line.startswith("AppointmentStatus:"):
                    appointment_data["AppointmentStatus"] = line.split(":")[1].strip()
            if appointment_data:  # Add the last appointment after finishing reading the file
                appointments_list.append(appointment_data)

        # Display all appointments
        if appointments_list:
            print("Appointments List:")
            for index, appointment in enumerate(appointments_list):
                print(f"\n{index + 1}. Appointment ID: {appointment['AppointmentID']}")
                print(f"   Donor ID: {appointment['DonorID']}")
                print(f"   Supervisor ID: {appointment['SupervisorID']}")
                print(f"   Date: {appointment['AppointmentDate']}")
                print(f"   Time: {appointment['AppointmentTime']}")
                print(f"   Status: {appointment['AppointmentStatus']}")

            # Approve or disapprove appointments
            while True:
                try:
                    appointment_index = int(input("\nEnter the number of the appointment to approve/unapprove (0 to exit): ").strip())
                    if appointment_index == 0:
                        print("Exiting... Goodbye!")
                        break

                    if 1 <= appointment_index <= len(appointments_list):
                        appointment = appointments_list[appointment_index - 1]
                        current_status = appointment["AppointmentStatus"]
                        new_status = "Approved" if current_status != "Approved" else "Unapproved"
                        appointment["AppointmentStatus"] = new_status

                        # Update the status in the file
                        with open("appointments.txt", "w") as appt_file:
                            for appt in appointments_list:
                                appt_file.write(f"AppointmentID: {appt['AppointmentID']}\n")
                                appt_file.write(f"DonorID: {appt['DonorID']}\n")
                                appt_file.write(f"SupervisorID: {appt['SupervisorID']}\n")
                                appt_file.write(f"AppointmentDate: {appt['AppointmentDate']}\n")
                                appt_file.write(f"AppointmentTime: {appt['AppointmentTime']}\n")
                                appt_file.write(f"AppointmentStatus: {appt['AppointmentStatus']}\n")
                                appt_file.write("----------------------------------------\n")

                        # Write the approved or unapproved appointment to the respective file
                        if appointment["AppointmentStatus"] == "Approved":
                            with open("approve.txt", "a") as approve_file:
                                approve_file.write(f"AppointmentID: {appointment['AppointmentID']}\n")
                                approve_file.write(f"DonorID: {appointment['DonorID']}\n")
                                approve_file.write(f"SupervisorID: {appointment['SupervisorID']}\n")
                                approve_file.write(f"AppointmentDate: {appointment['AppointmentDate']}\n")
                                approve_file.write(f"AppointmentTime: {appointment['AppointmentTime']}\n")
                                approve_file.write(f"AppointmentStatus: {appointment['AppointmentStatus']}\n")
                                approve_file.write("----------------------------------------\n")
                            print(f"Appointment ID {appointment['AppointmentID']} has been Approved.")
                        else:
                            with open("unapprove.txt", "a") as unapprove_file:
                                unapprove_file.write(f"AppointmentID: {appointment['AppointmentID']}\n")
                                unapprove_file.write(f"DonorID: {appointment['DonorID']}\n")
                                unapprove_file.write(f"SupervisorID: {appointment['SupervisorID']}\n")
                                unapprove_file.write(f"AppointmentDate: {appointment['AppointmentDate']}\n")
                                unapprove_file.write(f"AppointmentTime: {appointment['AppointmentTime']}\n")
                                unapprove_file.write(f"AppointmentStatus: {appointment['AppointmentStatus']}\n")
                                unapprove_file.write("----------------------------------------\n")
                            print(f"Appointment ID {appointment['AppointmentID']} has been Unapproved.")

                    else:
                        print("Invalid appointment number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            print("No appointments found.")
    except FileNotFoundError:
        print("The appointments' file does not exist yet. Please ensure that appointments have been scheduled.")



def donor_welcome():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1. Register a New Donor")
        print("2. Schedule an Appointment")
        print("3. View Medical Information")
        print("4.view approve or not approve")
        print("5. Exit")
        
        option = input("Please choose an option (1, 2, 3, 4): ").strip()
        
        if option == "1":
            register()
        elif option == "2":
            appointment()
        elif option == "3":
            print("Medical Information feature is under development.")
        elif option == "4":
           see_approval()
        elif option == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

def supervisor_welcome():
    while True:
        print("\nWelcome to Supervisor Bank X!")
        print("-----------------------------")
        print("1. View All Donors")
        print("2. Approve Appointment")
        print("3. Send Medical Information")
        print("4. Exit")
        
        option = input("Please choose an option (1, 2, 3, 4): ").strip()
        
        if option == "1":
            view_donors()
        elif option == "2":
            approval()
        elif option == "3":
            print("Medical Information feature is under development.")
        elif option == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

def welcome_message():
    print("Welcome to the Blood Bank System!")
    print("Please select your role:")
    print("1. Donor")
    print("2. Supervisor")

    role = input("Enter the number corresponding to your role: ")

    if role == '1':
        donor_welcome()
    elif role == '2':
        supervisor_welcome()
    else:
        print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    welcome_message()
