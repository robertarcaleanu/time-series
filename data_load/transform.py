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

        if len(parts) > 3:
            for part in parts:
                if part.lower() in list(month_names.keys()):
                    month = part
                elif part.isdigit() and len(part) == 4:
                    year = int(part)

            extension = parts[-1]
            file_name = f"{month}-{year}.{extension}"

            # Rename file with new file name
            try:
                os.rename(f"data/test/{file}", f"data/test/{file_name}")
                df = clean_report(path=f"data/test/{file_name}", month=month)
                df["Year"] = year
                df["Month"] = month_names[month]
                all_data = pd.concat([all_data, df])
            except Exception as e:
                print(f"Error renaming file {file} - {e}")
    try:
        all_data = all_data.drop_duplicates(subset=["Aeropuerto", "Year", "Month"])
        all_data = all_data.sort_values(by=["Year", "Month"])
        all_data.loc[all_data["Pax"] == "---", "Pax"] = 0
        all_data["Pax"] = all_data["Pax"].astype(float)
        all_data.loc[all_data["OP"] == "---", "OP"] = 0
        all_data["OP"] = all_data["OP"].astype(float)
        all_data.loc[all_data["Merc"] == "---", "Merc"] = 0
        all_data["Merc"] = all_data["Merc"].astype(float)

    except:
        print("Error dropping duplicates")

    return all_data

# Combine all files into a dataframe
def clean_report(path: str, month: str) -> pd.DataFrame:
    """This function cleans the report and returns a dataframe

    Args:
        path (str): path to the excel file
        month (str): month of the report

    Returns:
        pd.DataFrame: cleaned dataframe
    """
    hidden = False
    try:
        df = pd.read_excel(path, header=7)
        if df.shape[0] < 10:
            sheets = pd.read_excel(path, None)
            sheets = list(sheets.keys())
            sheet_name = [s for s in sheets if ("tráfico" in s.lower() or "trafico" in s.lower() or month in s.lower())]
            hidden = True
    except:
        # The sheet it's not the first
        sheets = pd.read_excel(path, None)
        sheets = list(sheets.keys())
        sheet_name = [s for s in sheets if ("tráfico" in s.lower() or "trafico" in s.lower() or month in s.lower())]
        df = pd.read_excel(path, sheet_name=sheet_name[0], header=7)
        hidden = True
    

    if hidden:
        header = 5
        while "aeropuertos" not in [str(col).lower().replace("\n", "") for col in df.columns]:
            df = pd.read_excel(path, sheet_name=sheet_name[0], header=header)
            header += 1
    else:
        header = 5
        while "aeropuertos" not in [str(col).lower().replace("\n", "") for col in df.columns]:
            df = pd.read_excel(path, header=header)
            header += 1

    unnamed_cols = [col for col in df.columns if col.lower().startswith("unnamed")]

    df = df.drop(unnamed_cols, axis=1)

    # Remove rows
    df.columns = [col.lower().replace("\n", "") for col in df.columns]
    df = df.dropna(subset=["aeropuertos"])
    df = df.dropna(subset=["total"])
    df = df[~df["aeropuertos"].str.lower().str.contains("total")]

    indices = [index for index, element in enumerate(df.columns) if "aeropuertos" in element]

    pax = df.iloc[:, [indices[0], indices[0] + 1]]
    pax.columns = ["Aeropuerto", "Pax"]
    pax["Aeropuerto"] = pax["Aeropuerto"].str.replace(r'[()*]', '', regex=True)
    pax["Aeropuerto"] = pax["Aeropuerto"].str.strip()

    op = df.iloc[:, [indices[1], indices[1] + 1]]
    op.columns = ["Aeropuerto", "OP"]
    op["Aeropuerto"] = op["Aeropuerto"].str.replace(r'[()*]', '', regex=True)
    op["Aeropuerto"] = op["Aeropuerto"].str.strip()

    merc = df.iloc[:, [indices[2], indices[2] + 1]]
    merc.columns = ["Aeropuerto", "Merc"]
    merc["Aeropuerto"] = merc["Aeropuerto"].str.replace(r'[()*]', '', regex=True)
    merc["Aeropuerto"] = merc["Aeropuerto"].str.strip()

    clean_df = pd.merge(pax, op, on="Aeropuerto", how="left")
    clean_df = pd.merge(clean_df, merc, on="Aeropuerto", how="left")

    return clean_df

def check_missing_data(df: pd.DataFrame) -> list:
    """This function checks for missing data in the dataframe.

    Args:
        df (pd.DataFrame): dataframe to check
    """
    missing_data = df.copy()
    # missing_data = all_data.copy()
    missing_data["date"] = missing_data["Year"].astype(str) + "-" + missing_data["Month"].astype(str)
    
    year_range = list(range(2004, 2025))
    month_range = list(range(1, 13))

    expected_data = []
    for year in year_range:
        for month in month_range:
            date = str(year) + "-" + str(month)
            expected_data.append(date)

    expected_data = expected_data[:-9]  # Remove last 9 months because have only until march 2024
    missing_month = set(expected_data) - set(missing_data["date"])
    
    return sorted(missing_month)

def format_airport_name(df: pd.DataFrame) -> pd.DataFrame:
    """This function formats the airport name in the dataframe.

    Args:
        df (pd.DataFrame): dataframe to format
    """
    map_airport_names = {
        "ALGECIRAS /HELIPUERTO": "ALGECIRAS-HELIPUERTO",
        "ALICANTE": "ALICANTE-ELCHE",
        "ALICANTE-ELCHE MIGUEL HDEZ.": "ALICANTE-ELCHE",
        "ALICANTE-ELCHE MIGUEL HERNANDEZ": "ALICANTE-ELCHE",
        "ALMERÍA": "ALMERIA",
        "BARCELONA-EL PRAT": "BARCELONA",
        "BARCELONA-EL PRAT J.T.": "BARCELONA",
        "CEUTA /HELIPUERTO": "CEUTA-HELIPUERTO",
        "CÓRDOBA": "CORDOBA",
        "FGL GRANADA-JAÉN": "FGL GRANADA-JAEN",
        "GRANADA": "FGL GRANADA-JAEN",
        "GIRONA": "GIRONA-COSTA BRAVA",
        "LANZAROTE CÉSAR MANRIQUE": "LANZAROTE",
        "LANZAROTE-CESAR MANRIQUE": "LANZAROTE",
        "LANZAROTE-CÉSAR MANRIQUE": "LANZAROTE",
        "LEÓN": "LEON",
        "MADRID-BARAJAS": "ADOLFO SUÁREZ MADRID-BARAJAS",
        "MALAGA-COSTA DEL SOL": "MALAGA",
        "MÁLAGA-COSTA DEL SOL": "MALAGA",
        "SAN SEBASTIÁN": "SAN SEBASTIAN",
        "SANTIAGO-ROSALÍA DE CASTRO": "SANTIAGO",
        "SEVE BALLESTEROS-SANTANDER": "SANTANDER",
        "TENERIFE NORTE-C. LA LAGUNA": "TENERIFE NORTE",
        "TENERIFE NORTE-CIUDAD LA LAGUNA": "TENERIFE NORTE",
        "TENERIFE-NORTE": "TENERIFE NORTE",
        "TENERIFE-SUR": "TENERIFE SUR",
        "MURCIA-SAN JAVIER": "AEROPUERTO INTL. REGIÓN MURCIA"
    }
    # df = all_data.copy()
    df["Aeropuerto"] = df["Aeropuerto"].map(map_airport_names).fillna(df["Aeropuerto"])
    df = df[df["Aeropuerto"] != "T O T A L"]

    return df

def add_missing_data(df: pd.DataFrame, missing_months: list) -> pd.DataFrame:
    """This function adds missing data to the dataframe.

    Args:
        df (pd.DataFrame): dataframe to add missing data
        missing_months (list): list of missing months
    """
    for month in missing_months:
        year = int(month.split("-")[0])
        month = int(month.split("-")[1])

        # Get list airports
        airp = df[(df["Year"] == year) & (df["Month"] == month + 1)][["Aeropuerto"]]
        airp["Year"] = year
        airp["Month"] = month

        # Merge with previous year
        airp = pd.merge(airp,
                        df[(df["Year"] == year - 1) & (df["Month"] == month)][["Aeropuerto", "Pax", "OP", "Merc"]],
                        how="left", on="Aeropuerto")
        # Merge with next year
        airp = pd.merge(airp,
                        df[(df["Year"] == year + 1) & (df["Month"] == month)][["Aeropuerto", "Pax", "OP", "Merc"]],
                        how="left", on="Aeropuerto", suffixes=("_prev", "_next"))
        airp["Pax"] = round((airp["Pax_prev"] + airp["Pax_next"]) / 2, 0)
        airp["OP"] = round((airp["OP_prev"] + airp["OP_next"]) / 2, 0)
        airp["Merc"] = round((airp["Merc_prev"] + airp["Merc_next"]) / 2, 0)
        airp = airp[['Aeropuerto', 'Pax', 'OP', 'Merc', 'Year', 'Month']]

        df = pd.concat([df, airp])

    return df