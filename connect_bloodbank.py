import pyodbc

# Define the connection string to connect to SQL Server
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost,1433;'  # Replace with your server address and port if necessary
    'DATABASE=BloodBank;'      # Replace with your database name
    'UID=your_username;'       # Replace with your SQL Server username
    'PWD=your_password;'       # Replace with your SQL Server password
)

try:
    # Establish the connection to SQL Server
    connection = pyodbc.connect(connection_string)
    print("Connection to BloodBank database established successfully!")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Example 1: Querying all donors
    cursor.execute("SELECT DonorID, FirstName, LastName FROM Donor")
    donors = cursor.fetchall()
    print("Donors in the database:")
    for donor in donors:
        print(f"Donor ID: {donor.DonorID}, Name: {donor.FirstName} {donor.LastName}")

    # Example 2: Inserting a new donor into the Donor table
    cursor.execute("""
        INSERT INTO Donor (FirstName, LastName, DateOfBirth, Gender, BloodType, Email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ('Jane', 'Doe', '1985-05-10', 'Female', 'O+', 'jane.doe@example.com'))
    connection.commit()
    print("New donor added successfully!")

    # Example 3: Querying after insertion
    cursor.execute("SELECT * FROM Donor WHERE FirstName = 'Jane'")
    new_donor = cursor.fetchall()
    print("Inserted donor details:")
    for donor in new_donor:
        print(donor)

except pyodbc.Error as e:
    print("Error:", e)

finally:
    # Close the connection
    if 'connection' in locals() and connection:
        connection.close()
        print("Connection closed.")
