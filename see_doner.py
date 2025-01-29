def view_doner():
    try:
        with open("donor_registration.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                donor_info = line.strip().split()
                print(f"Donor Name: {donor_info[0]} {donor_info[1]}, Blood Type: {donor_info[2]}, Date of Birth: {donor_info[3]}")
    except FileNotFoundError:
        print("The donors' file does not exist yet. Please register first.")
