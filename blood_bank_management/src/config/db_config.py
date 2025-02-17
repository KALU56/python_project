import pyodbc

def get_db_connection():
    try:
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=BloodBank;'
            'Trusted_Connection=yes;'
        )
    except pyodbc.Error as ex:
        print(f"Database error: {ex}")
        return None