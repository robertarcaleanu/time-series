import sqlite3
import pandas as pd

def store_data(path: str, df: pd.DataFrame) -> None:
    """This function stores the data from the file in a database.
    
    Args:
        path (str): The path to the database.
        df (pd.DataFrame): The data to be stored.
    
    Returns:
        None
    """

    conn = sqlite3.connect(path)
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS airports
                (Aeropuerto TEXT PRIMARY KEY,
                 Pax TEXT, 
                 OP TEXT,
                 Merc TEXT,
                 Year INTEGER,
                 Month INTEGER)''')
    
    # Insert values from DataFrame into the SQLite database
    df.to_sql('airports', conn, if_exists='replace', index=False)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()
    print("Data stored in database successfully!")