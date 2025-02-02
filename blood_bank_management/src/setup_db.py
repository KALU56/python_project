import sys
import os

# Add parent directory to the Python path so that src can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Now import db_config
from config.db_config import get_db_connection

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL template for checking if a table exists
    table_exists_template = '''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
    BEGIN
        {create_table_sql}
    END
    '''

    # Donor Table
    donor_sql = '''
    CREATE TABLE Donor (
        DonorID INT PRIMARY KEY IDENTITY(1,1),
        FirstName NVARCHAR(100),
        LastName NVARCHAR(100),
        DateOfBirth DATE,
        Gender NVARCHAR(10),
        BloodType NVARCHAR(5),
        Email NVARCHAR(100)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='Donor', create_table_sql=donor_sql))

    # DonorPhone Table
    donor_phone_sql = '''
    CREATE TABLE DonorPhone (
        DonorPhoneID INT PRIMARY KEY IDENTITY(1,1),
        DonorID INT,
        PhoneNumber NVARCHAR(15),
        PhoneType NVARCHAR(20),
        FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='DonorPhone', create_table_sql=donor_phone_sql))

    # DonorAddress Table
    donor_address_sql = '''
    CREATE TABLE DonorAddress (
        DonorAddressID INT PRIMARY KEY IDENTITY(1,1),
        DonorID INT,
        City NVARCHAR(100),
        Region NVARCHAR(100),
        Wereda NVARCHAR(100),
        Subcity NVARCHAR(100),
        FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='DonorAddress', create_table_sql=donor_address_sql))

    # BloodBank Table
    blood_bank_sql = '''
    CREATE TABLE BloodBank (
        BloodBankID INT PRIMARY KEY IDENTITY(1,1),
        BloodBankName NVARCHAR(100),
        BloodBankPhone NVARCHAR(15)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='BloodBank', create_table_sql=blood_bank_sql))

    # BloodBankAddress Table
    blood_bank_address_sql = '''
    CREATE TABLE BloodBankAddress (
        BloodBankAddressID INT PRIMARY KEY IDENTITY(1,1),
        BloodBankID INT,
        Branch NVARCHAR(100),
        BranchNumber NVARCHAR(50),
        City NVARCHAR(100),
        Region NVARCHAR(100),
        Wereda NVARCHAR(100),
        Subcity NVARCHAR(100),
        FOREIGN KEY (BloodBankID) REFERENCES BloodBank(BloodBankID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='BloodBankAddress', create_table_sql=blood_bank_address_sql))

    # Supervisor Table
    supervisor_sql = '''
    CREATE TABLE Supervisor (
        SupervisorID INT PRIMARY KEY IDENTITY(1,1),
        FirstName NVARCHAR(100),
        LastName NVARCHAR(100),
        Username NVARCHAR(50),
        Password NVARCHAR(255)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='Supervisor', create_table_sql=supervisor_sql))

    # Donation Table
    donation_sql = '''
    CREATE TABLE Donation (
        DonationID INT PRIMARY KEY IDENTITY(1,1),
        DonorID INT,
        DonationDate DATE,
        VolumeDonated FLOAT,
        BloodBankID INT,
        SupervisorID INT,
        FOREIGN KEY (DonorID) REFERENCES Donor(DonorID),
        FOREIGN KEY (BloodBankID) REFERENCES BloodBank(BloodBankID),
        FOREIGN KEY (SupervisorID) REFERENCES Supervisor(SupervisorID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='Donation', create_table_sql=donation_sql))

    # BloodUnit Table
    blood_unit_sql = '''
    CREATE TABLE BloodUnit (
        BloodUnitID INT PRIMARY KEY IDENTITY(1,1),
        BloodType NVARCHAR(5),
        CollectionDate DATE,
        ExpirationDate DATE,
        Status NVARCHAR(50),
        DonationID INT,
        FOREIGN KEY (DonationID) REFERENCES Donation(DonationID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='BloodUnit', create_table_sql=blood_unit_sql))

    # Appointment Table
    appointment_sql = '''
    CREATE TABLE Appointment (
        AppointmentID INT PRIMARY KEY IDENTITY(1,1),
        DonorID INT,
        SupervisorID INT,
        AppointmentDate DATE,
        AppointmentTime TIME,
        AppointmentStatus NVARCHAR(50),
        FOREIGN KEY (DonorID) REFERENCES Donor(DonorID),
        FOREIGN KEY (SupervisorID) REFERENCES Supervisor(SupervisorID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='Appointment', create_table_sql=appointment_sql))

    # MedicalHistory Table
    medical_history_sql = '''
    CREATE TABLE MedicalHistory (
        HistoryID INT PRIMARY KEY IDENTITY(1,1),
        DonorID INT,
        HIV BIT,
        Syphilis BIT,
        Hepatitis_B BIT,
        Hepatitis_C BIT,
        SugarLevel FLOAT,
        OutcomeDetails NVARCHAR(255),
        FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='MedicalHistory', create_table_sql=medical_history_sql))

    # HealthState Table
    health_state_sql = '''
    CREATE TABLE HealthState (
        HealthStateID INT PRIMARY KEY IDENTITY(1,1),
        DonorID INT,
        DonationID INT,
        Weight FLOAT,
        SugarLevel FLOAT,
        BloodPressure NVARCHAR(50),
        DateChecked DATE,
        TimeChecked TIME,
        FOREIGN KEY (DonorID) REFERENCES Donor(DonorID),
        FOREIGN KEY (DonationID) REFERENCES Donation(DonationID)
    )
    '''
    cursor.execute(table_exists_template.format(table_name='HealthState', create_table_sql=health_state_sql))

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables created successfully!")

if __name__ == "__main__":
    create_tables()
