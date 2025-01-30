import try.see_doner as see_doner

def supervisor_welcome():
    while True:
        print("\nWelcome to Donor Bank X!")
        print("-------------------------")
        print("1. all doner see")
        print("2. approved the appointment")
        print("3. send Medical Information")
        print("4. Exit")
        
        option = input("Please choose an option (1, 2, 3, 4): ").strip()
        
        if option == "1":
            see_doner.view_doner()
        elif option == "2":
            return 1
        elif option == "3":
            print("Medical Information feature is under development.")
        elif option == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    supervisor_welcome()
  
