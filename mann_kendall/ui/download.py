import base64
from io import BytesIO
from datetime import datetime
from random import randint

import pandas as pd


def to_excel(dataframe: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to Excel format and returns it as bytes.

    Args:
        dataframe (pd.DataFrame): DataFrame to be converted to Excel format.

    Returns:
        bytes: Excel file as bytes.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Sheet1")
    return output.getvalue()


def get_table_download_link(dataframe: pd.DataFrame, filename: str = "mann_kendall") -> str:
    """
    Generates a button to download a file.

    Args:
        dataframe (pd.DataFrame): DataFrame to be downloaded.
        filename (str, optional): Name of the file to download. Defaults to "mann_kendall".

    Returns:
        str: HTML string representing a button with a href as stream.
    """
    val = to_excel(dataframe)
    b64 = base64.b64encode(val)
    
    return (
        '<p style="text-align:center;">'
        f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
        f'download="{filename}.xlsx">Download Excel file</a></p>'
    )


def generate_output_filename(original_filename: str = None) -> str:
    """
    Generates a unique filename for the output file.
    
    Args:
        original_filename (str, optional): Original filename to base the new name on.
            If None, a generic name will be used.
            
    Returns:
        str: Generated filename with timestamp and random number
    """
    today = datetime.today().strftime("%Y_%m_%d")
    random_number = randint(1000, 5000)
    
    if original_filename:
        # Extract just the filename without path or extension
        base_name = original_filename.split("/")[-1].split('.')[0]
        return f"{base_name}_{today}_{random_number}"
    
    return f"mann_kendall_{today}_{random_number}"


def save_to_excel(dataframe: pd.DataFrame, filename: str) -> str:
    """
    Saves DataFrame to Excel file with a unique filename.
    
    Args:
        dataframe (pd.DataFrame): DataFrame to save
        filename (str): Base filename
        
    Returns:
        str: Full path to the saved file
    """
    output_filename = f"output_tables/{generate_output_filename(filename)}.xlsx"
    
    dataframe.to_excel(output_filename, index=False, sheet_name="mann_kendall")
    return output_filename