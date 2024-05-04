from data_load.transform import rename_files, check_missing_data
import warnings

def main():
    # Suppress all warnings
    warnings.filterwarnings("ignore")
    all_data = rename_files()
    warnings.resetwarnings()
    missing_months = check_missing_data(all_data)
    len(missing_months)