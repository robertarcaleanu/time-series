from data_load.transform import rename_files, check_missing_data, format_airport_name
from data_load.load import store_data

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

    # Store data in DDBB
    try:
        logging.info("Data stored in database successfully!")
        store_data(path="data/test/ddbb/airports.db", df=all_data)
    except Exception as e:
        logging.error("Data has not been stored in database: {}".format(e))
        raise e

    # Add missing months to the data
    missing_months = check_missing_data(all_data)
    len(missing_months)