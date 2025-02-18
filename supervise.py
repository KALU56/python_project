import doners_i
def approve_appointments():
    try:
        with open("appointments.txt", "r") as file:
            appointments = file.read().strip().split("----------------------------------------\n")
        
        pending_appointments = []
        for appointment in appointments:
            if "AppointmentStatus: Scheduled" in appointment:
                pending_appointments.append(appointment)
        
        if not pending_appointments:
            print("No pending appointments to approve or disapprove.")
            return
        
        for index, appointment in enumerate(pending_appointments):
            print(f"\nAppointment {index + 1}:")
            print(appointment.strip())
            
            decision = input("Approve (A), Disapprove (D), or Exit (E) the approval process? (A/D/E): ").strip().upper()
            
            if decision == 'A':
                appointment = appointment.replace("AppointmentStatus: Scheduled", "AppointmentStatus: Approved")
                print("Appointment approved.")
            elif decision == 'D':
                appointment = appointment.replace("AppointmentStatus: Scheduled", "AppointmentStatus: Disapproved")
                print("Appointment disapproved.")
            elif decision == 'E':
                print("Exiting the appointment approval process.")
                break  # Exit the loop immediately
            else:
                print("Invalid input. Skipping this appointment.")
            
            # Update the appointment in the main list if not exiting
            if decision in ['A', 'D']:
                appointments[appointments.index(pending_appointments[index])] = appointment
        
        # Write the updated appointments back to the file only if changes were made
        with open("appointments.txt", "w") as file:
            for appointment in appointments:
                if appointment.strip():  # Avoid writing empty lines
                    file.write(appointment.strip() + "\n----------------------------------------\n")
        
        print("All updates saved successfully!")

    except FileNotFoundError:
        print("No appointments found. Please schedule appointments first.")
    except Exception as e:
        print(f"An error occurred: {e}")
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
import uuid
import uuid

def record_medical_history():
    email = input("Enter Donor Email: ").strip()
    
    # Supervisor inputs medical conditions
    print("\nEnter Medical Conditions (1 = Yes, 0 = No):")
    hiv = input("HIV (1/0): ").strip()
    syphilis = input("Syphilis (1/0): ").strip()
    hepatitis_b = input("Hepatitis B (1/0): ").strip()
    hepatitis_c = input("Hepatitis C (1/0): ").strip()
    
    # Validate conditions (must be 1 or 0)
    if not all(condition in ['0', '1'] for condition in [hiv, syphilis, hepatitis_b, hepatitis_c]):
        print("Invalid input for medical conditions. Please enter 1 or 0.")
        return

    # Supervisor inputs sugar level and outcome details
    sugar_level = input("Enter Sugar Level: ").strip()
    outcome_details = input("Enter Outcome Details: ").strip()
    
    history_id = str(uuid.uuid4())  # Unique identifier for medical history
    
    # Save to file
    try:
        with open("medical_history.txt", "a") as file:
            file.write(f"HistoryID: {history_id}\n")
            file.write(f"Email: {email}\n")
            file.write(f"HIV: {hiv}\n")
            file.write(f"Syphilis: {syphilis}\n")
            file.write(f"Hepatitis_B: {hepatitis_b}\n")
            file.write(f"Hepatitis_C: {hepatitis_c}\n")
            file.write(f"SugarLevel: {sugar_level}\n")
            file.write(f"OutcomeDetails: {outcome_details}\n")
            file.write("----------------------------------------\n")
        
        print("Medical history recorded successfully!")

        # Show confirmation of history recorded
        print(f"\nDonor {email} has been successfully updated with the following details:")
        print(f"HIV: {hiv}, Syphilis: {syphilis}, Hepatitis B: {hepatitis_b}, Hepatitis C: {hepatitis_c}")
        print(f"Sugar Level: {sugar_level}")
        print(f"Outcome Details: {outcome_details}")

        # Notify donor (can be shown on console or implemented with actual email)
        # Calling a function that could notify the donor (replace with actual email logic if needed)
        doners_i.notify_donor(email)
    
    except Exception as e:
        print(f"Error saving medical history: {e}")
import uuid
from datetime import datetime

def record_health_state():
    # Supervisor inputs DonorID, DonationID, and health check details
    donor_id = input("Enter Donor ID: ").strip()
    donation_id = input("Enter Donation ID: ").strip()

    # Supervisor inputs weight, sugar level, and blood pressure
    weight = input("Enter Donor's Weight (kg): ").strip()
    sugar_level = input("Enter Donor's Sugar Level: ").strip()
    blood_pressure = input("Enter Donor's Blood Pressure: ").strip()

    # Supervisor inputs the date and time of the health check
    date_checked = input("Enter Date of Health Check (YYYY-MM-DD): ").strip()
    time_checked = input("Enter Time of Health Check (HH:MM): ").strip()

    # Validate the date and time format
    try:
        datetime.strptime(date_checked, "%Y-%m-%d")  # Validate the date format
        datetime.strptime(time_checked, "%H:%M")     # Validate the time format
    except ValueError:
        print("Invalid date or time format. Please enter in the correct format.")
        return

    health_state_id = str(uuid.uuid4())  # Unique identifier for health state record

    # Save the health state record to a file
    try:
        with open("health_state.txt", "a") as file:
            file.write(f"HealthStateID: {health_state_id}\n")
            file.write(f"DonorID: {donor_id}\n")
            file.write(f"DonationID: {donation_id}\n")
            file.write(f"Weight: {weight}\n")
            file.write(f"SugarLevel: {sugar_level}\n")
            file.write(f"BloodPressure: {blood_pressure}\n")
            file.write(f"DateChecked: {date_checked}\n")
            file.write(f"TimeChecked: {time_checked}\n")
            file.write("----------------------------------------\n")

        print("Health state recorded successfully!")
    except Exception as e:
        print(f"Error saving health state: {e}")
