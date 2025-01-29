class Donor:
    def __init__(self, donor_id, first_name, last_name, date_of_birth, gender, blood_type, email):
        self.donor_id = donor_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.blood_type = blood_type
        self.email = email
        self.phones = []
        self.addresses = []  
        self.medical_history = None  

    def register(self, phone, address):
        self.phones.append(phone)
        self.addresses.append(address)

    def view_medical_history(self):
        return self.medical_history

    def view_health_states(self):
        return [hs for hs in HealthState.all_states if hs.donor_id == self.donor_id]
doner_name=input("please enter your name")
doner_last_name=input("please enter your last name")
doner_date_of_birth=input("please enter date of birth")
doner_gender=input("please enter your gender(male or female)")

donor_blood_type=input("please enter your name(A,A+,A-,B,B+,B-,O,O+,O-,AB)")

donor_email=input("please enter your email address")
D1=Donor(doner_name,doner_last_name,doner_date_of_birth,doner_gender,donor_blood_type,donor_email)

class DonorPhone:
    def __init__(self, phone_id, donor_id, phone_number, phone_type):
        self.phone_id = phone_id
        self.donor_id = donor_id
        self.phone_number = phone_number
        self.phone_type = phone_type
doner_phone_id=input("please enter your name")
doner_donor_=input("please enter your last name")
doner_date_of_birth=input("please enter date of birth")
doner_gender=input("please enter your gender(male or female)")

donor_blood_type=input("please enter your name(A,A+,A-,B,B+,B-,O,O+,O-,AB)")

donor_email=input("please enter your email address")

class DonorAddress:
    def __init__(self, address_id, donor_id, city, region, wereda, subcity):
        self.address_id = address_id
        self.donor_id = donor_id
        self.city = city
        self.region = region
        self.wereda = wereda
        self.subcity = subcity


class BloodBank:
    def __init__(self, blood_bank_id, name, phone):
        self.blood_bank_id = blood_bank_id
        self.name = name
        self.phone = phone
        self.addresses = []  # List of BloodBankAddress objects

    def add_address(self, address):
        self.addresses.append(address)


class BloodBankAddress:
    def __init__(self, address_id, blood_bank_id, branch, branch_number):
        self.address_id = address_id
        self.blood_bank_id = blood_bank_id
        self.branch = branch
        self.branch_number = branch_number


class Donation:
    def __init__(self, donation_id, donor_id, donation_date, volume_donated, blood_bank_id, supervisor_id):
        self.donation_id = donation_id
        self.donor_id = donor_id
        self.donation_date = donation_date
        self.volume_donated = volume_donated
        self.blood_bank_id = blood_bank_id
        self.supervisor_id = supervisor_id


class BloodUnit:
    def __init__(self, blood_unit_id, donation_id, blood_type, collection_date, expiration_date, status):
        self.blood_unit_id = blood_unit_id
        self.donation_id = donation_id
        self.blood_type = blood_type
        self.collection_date = collection_date
        self.expiration_date = expiration_date
        self.status = status


class Supervisor:
    def __init__(self, supervisor_id, first_name, last_name, username, password):
        self.supervisor_id = supervisor_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def supervise_donor(self, donor):
        return donor

    def manage_appointment(self, appointment, status):
        appointment.status = status

    def send_medical_history(self, donor, medical_history):
        donor.medical_history = medical_history

    def add_donation(self, donation):
        Donation.all_donations.append(donation)

    def add_blood_unit(self, blood_unit):
        BloodUnit.all_units.append(blood_unit)


class Appointment:
    def __init__(self, appointment_id, donor_id, supervisor_id, appointment_date, appointment_time, status):
        self.appointment_id = appointment_id
        self.donor_id = donor_id
        self.supervisor_id = supervisor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status


class MedicalHistory:
    def __init__(self, history_id, donor_id, hiv, syphilis, hepatitis_b, hepatitis_c, outcome_details):
        self.history_id = history_id
        self.donor_id = donor_id
        self.hiv = hiv
        self.syphilis = syphilis
        self.hepatitis_b = hepatitis_b
        self.hepatitis_c = hepatitis_c
        self.outcome_details = outcome_details


class HealthState:
    all_states = []

    def __init__(self, health_state_id, donor_id, donation_id, weight, sugar_level, blood_pressure, date_checked, time_checked):
        self.health_state_id = health_state_id
        self.donor_id = donor_id
        self.donation_id = donation_id
        self.weight = weight
        self.sugar_level = sugar_level
        self.blood_pressure = blood_pressure
        self.date_checked = date_checked
        self.time_checked = time_checked
        HealthState.all_states.append(self)


def main():
    print("Welcome to the Blood Bank Management System")
    print("Please choose your role:")
    print("1. Supervisor")
    print("2. Donor")
    role_choice = input("Enter your choice (1 or 2): ")

    if role_choice == "1":
        print("Supervisor Options:")
        print("1. Approve/Disapprove Appointments")
        print("2. Add Donations and Blood Units")
        print("3. Manage Donor Medical History")
        supervisor_choice = input("Enter your choice: ")

        if supervisor_choice == "1":
            print("Managing appointments...")
            # Add appointment management logic here
        elif supervisor_choice == "2":
            print("Adding donations and blood units...")
            # Add donation and blood unit logic here
        elif supervisor_choice == "3":
            print("Managing donor medical history...")
            # Add medical history management logic here
        else:
            print("Invalid choice!")

    elif role_choice == "2":
        print("Donor Options:")
        print("1. Register as a Donor")
        print("2. View Medical History")
        print("3. View Health States")
        donor_choice = input("Enter your choice: ")

        if donor_choice == "1":
            print("Registering as a donor...")
            # Add donor registration logic here
        elif donor_choice == "2":
            print("Viewing medical history...")
            # Add logic to view medical history
        elif donor_choice == "3":
            print("Viewing health states...")
            # Add logic to view health states
        else:
            print("Invalid choice!")

    else:
        print("Invalid role choice! Exiting system.")


if __name__ == "__main__":
    main()
