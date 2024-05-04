import sqlite3
import pandas as pd
import polars as pl

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
                 Pax FLOAT, 
                 OP FLOAT,
                 Merc FLOAT,
                 Year INTEGER,
                 Month INTEGER)''')
    
    # Insert values from DataFrame into the SQLite database
    df.to_sql('airports', conn, if_exists='replace', index=False)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()
    print("Data stored in database successfully!")

def get_data(path: str) -> pl.DataFrame:
    """This function loads the data from the database.

    Args:
        path (str): The path to the database.

    Returns:
        pl.DataFrame: The data from the database.
    """
    conn = sqlite3.connect(path)
    df = pl.read_database(query="SELECT * FROM airports", connection=conn)
    conn.close()

    return df