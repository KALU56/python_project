from src.config.db_config import get_db_connection

def view_donors():
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM Donor')
                donors = cursor.fetchall()

                if donors:
                    for donor in donors:
                        print(f"DonorID: {donor[0]}, Name: {donor[1]} {donor[2]}, Blood Type: {donor[5]}, Email: {donor[6]}")
                else:
                    print("No donors found.")

    except Exception as e:
        print(f"An error occurred while viewing donors: {e}")


def approve_appointments():
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cursor:
                appointment_id = input("Enter Appointment ID to approve: ").strip()

                sql = "UPDATE Appointment SET AppointmentStatus = ? WHERE AppointmentID = ?"
                cursor.execute(sql, ('Approved', appointment_id))
                conn.commit()
                print(f"Appointment {appointment_id} approved!")

    except Exception as e:
        print(f"An error occurred while approving appointments: {e}")


def record_medical_history():
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cursor:
                donor_id = input("Enter Donor ID: ").strip()
                hiv = input("HIV (1 for Yes, 0 for No): ").strip()
                syphilis = input("Syphilis (1 for Yes, 0 for No): ").strip()
                hepatitis_b = input("Hepatitis B (1 for Yes, 0 for No): ").strip()
                hepatitis_c = input("Hepatitis C (1 for Yes, 0 for No): ").strip()
                sugar_level = input("Sugar Level: ").strip()
                outcome_details = input("Outcome Details: ").strip()

                sql = """
                    INSERT INTO MedicalHistory (DonorID, HIV, Syphilis, Hepatitis_B, Hepatitis_C, SugarLevel, OutcomeDetails)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql, (donor_id, int(hiv), int(syphilis), int(hepatitis_b), int(hepatitis_c), float(sugar_level), outcome_details)) # Convert to correct types
                conn.commit()
                print("Medical history recorded successfully!")

    except Exception as e:
        print(f"An error occurred while recording medical history: {e}")


def record_health_state():
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cursor:
                donor_id = input("Enter Donor ID: ").strip()
                donation_id = input("Enter Donation ID: ").strip()
                weight = input("Enter Weight: ").strip()
                sugar_level = input("Enter Sugar Level: ").strip()
                blood_pressure = input("Enter Blood Pressure: ").strip()
                date_checked = input("Enter Date Checked (YYYY-MM-DD): ").strip()
                time_checked = input("Enter Time Checked (HH:MM:SS): ").strip()

                sql = """
                    INSERT INTO HealthState (DonorID, DonationID, Weight, SugarLevel, BloodPressure, DateChecked, TimeChecked)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql, (donor_id, donation_id, float(weight), float(sugar_level), blood_pressure, date_checked, time_checked))  # Convert types
                conn.commit()
                print("Health state recorded successfully!")

    except Exception as e:
        print(f"An error occurred while recording health state: {e}")