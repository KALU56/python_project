from src.config.db_config import get_db_connection

def register():
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:  # Use 'with' to ensure connection closure
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
            gender = input("Enter Gender (M/F): ").strip()
            blood_type = input("Enter Blood Type (A+, B-, etc.): ").strip()
            email = input("Enter Email: ").strip()

            cursor.execute('''
            INSERT INTO Donor (FirstName, LastName, DateOfBirth, Gender, BloodType, Email)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, date_of_birth, gender, blood_type, email))

            conn.commit()
            print("Donor registered successfully!")
    except Exception as e:
        print(f"An error occurred in register: {e}")
    finally:
        if conn:
            conn.close()  # Ensure connection is closed even if exception occurs


# ... (Other donor functions - appointment, check_appointment_status, notify_donor - follow the same structure as register())

def appointment():
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            donor_id = input("Enter Donor ID: ").strip()
            supervisor_id = input("Enter Supervisor ID: ").strip()
            appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ").strip()
            appointment_time = input("Enter Appointment Time (HH:MM:SS): ").strip()

            cursor.execute('''
            INSERT INTO Appointment (DonorID, SupervisorID, AppointmentDate, AppointmentTime, AppointmentStatus)
            VALUES (?, ?, ?, ?, ?)
            ''', (donor_id, supervisor_id, appointment_date, appointment_time, 'Pending'))

            conn.commit()
            print("Appointment scheduled successfully!")
    except Exception as e:
        print(f"An error occurred in appointment: {e}")
    finally:
        if conn:
            conn.close()

def check_appointment_status():
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            donor_id = input("Enter Donor ID: ").strip()

            cursor.execute('''
            SELECT AppointmentStatus FROM Appointment WHERE DonorID = ?
            ''', (donor_id,))
            status = cursor.fetchone()

            if status:
                print(f"Appointment Status: {status[0]}")
            else:
                print("No appointment found for this donor.")
    except Exception as e:
        print(f"An error occurred in check_appointment_status: {e}")
    finally:
        if conn:
            conn.close()

def notify_donor():
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            donor_id = input("Enter Donor ID: ").strip()

            cursor.execute('''
            SELECT * FROM MedicalHistory WHERE DonorID = ?
            ''', (donor_id,))
            medical_info = cursor.fetchone()

            if medical_info:
                print(f"Medical Information: HIV: {medical_info[2]}, Syphilis: {medical_info[3]}, Hepatitis_B: {medical_info[4]}, Hepatitis_C: {medical_info[5]}, SugarLevel: {medical_info[6]}")
            else:
                print("No medical information found for this donor.")
    except Exception as e:
        print(f"An error occurred in notify_donor: {e}")
    finally:
        if conn:
            conn.close()