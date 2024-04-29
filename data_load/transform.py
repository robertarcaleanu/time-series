import os
import pandas as pd


# list all files in a directory
def rename_files() -> pd.DataFrame:
    """This function renames all files in the test folder to a more readable format.
    """
    files = os.listdir('data/test')
    month_names = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    all_data = pd.DataFrame()
    for file in files:
        file_mod = file.lower()
        file_mod = file_mod.replace("-", "_") 
        file_mod = file_mod.replace("+", "_")
        file_mod = file_mod.replace(".", "_")
        file_mod = file_mod.replace(" ", "_")
        file_mod = file_mod.replace("(", "_")
        file_mod = file_mod.replace(")", "_")

        parts = file_mod.split("_")

        for part in parts:
            if part.lower() in list(month_names.keys()):
                month = part
            elif part.isdigit() and len(part) == 4:
                year = int(part)

        extension = parts[-1]
        file_name = f"{month}_{year}.{extension}"

        # Rename file with new file name
        try:
            os.rename(f"data/test/{file}", f"data/test/{file_name}")
            df = clean_report(path=f"data/test/{file_name}")
            df["Year"] = year
            df["Month"] = month_names[month]
            all_data = pd.concat([all_data, df])
        except:
            print(f"Error renaming file {file}")

    all_data = all_data.drop_duplicates(subset=["Aeropuerto", "Year", "Month"])

    return all_data


# Combine all files into a dataframe
def clean_report(path: str) -> pd.DataFrame:
    """This function cleans the report and returns a dataframe

    Args:
        path (str): path to the excel file

    Returns:
        pd.DataFrame: cleaned dataframe
    """
    df = pd.read_excel(path, header=7)
    unnamed_cols = [col for col in df.columns if col.lower().startswith("unnamed")]

    df = df.drop(unnamed_cols, axis=1)

    # Remove rows
    df = df.dropna(subset=["\nAeropuertos"])
    df = df.dropna(subset=["\nTotal"])
    df = df[~df["\nAeropuertos"].str.lower().str.contains("total")]

    pax = df.iloc[:, [0, 1]]
    pax.columns = ["Aeropuerto", "Pax"]
    op = df.iloc[:, [3, 4]]
    op.columns = ["Aeropuerto", "OP"]
    merc = df.iloc[:, [6, 7]]
    merc.columns = ["Aeropuerto", "Merc"]

    clean_df = pd.merge(pax, op, on="Aeropuerto", how="left")
    clean_df = pd.merge(clean_df, merc, on="Aeropuerto", how="left")

    return clean_df