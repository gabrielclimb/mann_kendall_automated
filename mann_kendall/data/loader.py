from typing import BinaryIO, Union

import pandas as pd


def load_excel_data(file_content: Union[str, bytes, BinaryIO]) -> pd.DataFrame:
    """
    Loads data from an Excel file into a pandas DataFrame.
    
    Args:
        file_content (Union[str, bytes, BinaryIO]): 
            Either a file path string, bytes object containing Excel data,
            or a file-like object.
            
    Returns:
        pd.DataFrame: DataFrame containing the loaded data with index_col=0 and no header
        
    Raises:
        pd.errors.EmptyDataError: If the file is empty
        pd.errors.ParserError: If the file cannot be parsed as an Excel file
        ValueError: If the file format is invalid
    """
    try:
        return pd.read_excel(file_content, header=None, index_col=0)
    except Exception as e:
        # Re-raise with more context
        raise type(e)(f"Error loading Excel file: {str(e)}")


def validate_input_format(df: pd.DataFrame) -> bool:
    """
    Validates that the input DataFrame has the expected format:
    - First row should be well names
    - First column should be dates
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        
    Returns:
        bool: True if valid, raises exception otherwise
        
    Raises:
        ValueError: If DataFrame does not have the expected format
    """
    # Check that first row (index 0) contains well names
    if df.shape[1] < 2:
        raise ValueError("Input file must have at least two columns (date and one well)")
    
    # Check that first column (index) contains dates
    if not isinstance(df.index[0], (str, pd.Timestamp)) and not pd.isna(df.index[0]):
        raise ValueError("First column must contain dates or date-like strings")
    
    return True