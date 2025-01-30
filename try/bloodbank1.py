
def welcome_message():
    print("Welcome to the Blood Bank System!")
    print("Please select your role:")

    print("1. Donor")
    print("2. Supervisor")

    role = input("Enter the number corresponding to your role: ")

    if role == '1':
        print("Welcome, Blood Bank Management!")
       
    elif role == '2':
        print("Welcome, Donor!")
        doner()
    elif role == '3':
        print("Welcome, Supervisor!")
        supervisor()
    else:
        print("Invalid input. Please enter 1, 2, or 3.")
