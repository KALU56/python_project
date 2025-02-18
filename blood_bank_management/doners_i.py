import uuid
from datetime import datetime
import re
def find_donor_by_email(email):
    """Search donor_registration.txt for a donor by email and return DonorID."""
    try:
        with open("donor_registration.txt", "r") as file:
            donor_id = None
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("Email:") and lines[i].strip().split()[1] == email:
                    # Extract DonorID from earlier lines
                    for j in range(max(0, i - 10), i):  # Look up to 10 lines back for DonorID
                        if lines[j].startswith("DonorID:"):
                            donor_id = lines[j].strip().split()[1]
                            return donor_id
        return None  # If no donor is found
    except FileNotFoundError:
        print("Error: Donor registration file not found.")
        return None

def validate_date_of_birth(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.today() - birth_date).days // 365
        return age >= 18
    except ValueError:
        return False
def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
def validate_time(time_str):
    """Validate time format (HH:MM)."""
    from datetime import datetime
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def validate_phone_number(phone_number):
    return re.match(r"^(09|07)\d{8}$", phone_number) is not None

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

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
        donor_welcome()

def donor_welcome():
    print("Welcome, donor! Your information has been successfully recorded.")
def check_appointment_status():
    email = input("Enter your email to check appointment status: ").strip()

    if not validate_email(email):
        print("Invalid email format. Please enter a valid email address.")
        return

    try:
        with open("appointments.txt", "r") as file:
            appointments = file.read().strip().split("----------------------------------------\n")

        found = False
        for appointment in appointments:
            if f"Email: {email}" in appointment:
                found = True
                # Display appointment details
                print("\nYour Appointment Details:")
                lines = appointment.strip().split("\n")
                for line in lines:
                    if "AppointmentStatus:" in line:
                        status = line.split(":")[1].strip()
                        print(f"Status: {status}")
                    elif "AppointmentDate:" in line or "AppointmentTime:" in line:
                        print(line)

        if not found:
            print("No appointment found for this email. Please schedule an appointment first.")

    except FileNotFoundError:
        print("No appointments found. Please schedule an appointment first.")
    except Exception as e:
        print(f"An error occurred: {e}")
def appointment():
    email = input("Enter your email address: ").strip()

    if not validate_email(email):
        print("Invalid email format. Please enter a valid email address.")
        return

    donor_id = find_donor_by_email(email)
    if not donor_id:
        print("No donor found with this email. Please register first.")
        register.register()  # Call register if donor is not found
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
            appt_file.write(f"Email: {email}\n")  # Store donor email
            appt_file.write(f"SupervisorID: {supervisor_id}\n")
            appt_file.write(f"AppointmentDate: {appointment_date}\n")
            appt_file.write(f"AppointmentTime: {appointment_time}\n")
            appt_file.write(f"AppointmentStatus: {appointment_status}\n")
            appt_file.write("----------------------------------------\n")

        print("Your appointment has been scheduled successfully!")

    except Exception as e:
        print(f"Error saving appointment: {e}")
def notify_donor():
    # Ask the donor for their email
    email = input("Please enter your email to view your medical history: ").strip()

    try:
        # Read the medical history file
        with open("medical_history.txt", "r") as file:
            lines = file.readlines()
        
        # Flag to check if the email's medical history is found
        found = False
        donor_history = []

        # Loop through the file lines and extract the medical history for the provided email
        for line in lines:
            if line.startswith("Email:"):
                current_email = line.split(":")[1].strip()
                if current_email == email:
                    found = True
                    donor_history.append(f"Medical History for {email}:")
            if found:
                donor_history.append(line.strip())  # Add the rest of the medical history details
            if line.startswith("----------------------------------------") and found:
                found = False  # Reset flag after a complete record
                break  # Stop after reading the donor's complete record

        # Display the medical history
        if donor_history:
            print("\n".join(donor_history))
        else:
            print(f"No medical history found for email: {email}")

    except FileNotFoundError:
        print("Medical history file not found. Please ensure it exists.")
    except Exception as e:
        print(f"Error accessing medical history: {e}")

