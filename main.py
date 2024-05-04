from data_load.transform import rename_files, check_missing_data, format_airport_name, add_missing_data
from data_load.load import store_data, get_data

import warnings
import logging

def main():
    # Suppress all warnings
    warnings.filterwarnings("ignore")
    all_data = rename_files()
    warnings.resetwarnings()

    try:
        logging.info("Data formated successfully")
        all_data = format_airport_name(all_data)
    except Exception as e:
        logging.error("Data has not been formated: {}".format(e))

    # Add missing months to the data
    missing_months = check_missing_data(all_data)
    len(missing_months)
    try:
        logging.info("Missing months data added successfully!")
        all_data = add_missing_data(all_data, missing_months)
    except Exception as e:
        logging.error("Missing months data has not been added: {}".format(e))

    # Store data in DDBB
    try:
        logging.info("Data stored in database successfully!")
        store_data(path="C:/Users/rober/OneDrive/Escriptori/DataSets/Time-Series/time-series/data/ddbb/airports.db", df=all_data)
    except Exception as e:
        logging.error("Data has not been stored in database: {}".format(e))
        raise e

    try:
        logging.info("Data retrieved from database successfully!")
        all_data = get_data(path="C:/Users/rober/OneDrive/Escriptori/DataSets/Time-Series/time-series/data/ddbb/airports.db")
    except Exception as e:
        logging.error("Data has not been retrieved from database: {}".format(e))
    
    