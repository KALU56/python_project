import uuid
from datetime import datetime
import re

def validate_date_of_birth(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.today() - birth_date).days // 365
        return age >= 18
    except ValueError:
        return False

def validate_phone_number(phone_number):
    return re.match(r"^(09|07)\d{8}$", phone_number) is not None

def register():
    with open("donor.txt", "a") as file:
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