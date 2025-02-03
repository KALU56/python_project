import pyodbc

def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=BloodBank;'
            'Trusted_Connection=yes;'
        )
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database connection error: {sqlstate}")  # More informative error message
        return None  # Return None to indicate failure