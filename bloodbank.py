class Donor:
    def __init__(self, donor_id, first_name, last_name, date_of_birth, gender, blood_type, email):
        self.donor_id = donor_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.blood_type = blood_type
        self.email = email
        self.phones = []  # List of DonorPhone objects
        self.addresses = []  # List of DonorAddress objects
        self.medical_history = None  # MedicalHistory object

class DonorPhone:
    def __init__(self, phone_id, donor_id, phone_number, phone_type):
        self.phone_id = phone_id
        self.donor_id = donor_id
        self.phone_number = phone_number
        self.phone_type = phone_type

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
    def __init__(self, health_state_id, donor_id, donation_id, weight, sugar_level, blood_pressure, date_checked, time_checked):
        self.health_state_id = health_state_id
        self.donor_id = donor_id
        self.donation_id = donation_id
        self.weight = weight
        self.sugar_level = sugar_level
        self.blood_pressure = blood_pressure
        self.date_checked = date_checked
        self.time_checked = time_checked

# Example of creating instances:
donor = Donor(1, "John", "Doe", "1990-01-01", "Male", "O+", "john@example.com")
donor_phone = DonorPhone(101, donor.donor_id, "1234567890", "Mobile")
donor_address = DonorAddress(201, donor.donor_id, "CityA", "RegionA", "WeredaA", "SubcityA")
blood_bank = BloodBank(301, "BloodBankX", "9876543210")
medical_history = MedicalHistory(901, donor.donor_id, False, False, True, False, "Healthy")

# Adding relationships
donor.phones.append(donor_phone)
donor.addresses.append(donor_address)
donor.medical_history = medical_history

# Print donor details
print(f"Donor: {donor.first_name} {donor.last_name}, Blood Type: {donor.blood_type}")

    