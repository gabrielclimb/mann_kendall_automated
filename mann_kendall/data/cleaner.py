from typing import Optional, Union

import pandas as pd


def string_to_float(x: Union[str, float]) -> float:
    """
    Converts a string representation of a number to a float.
    Handles special cases like "<0.01" by removing the "<" symbol.

    Args:
        x (Union[str, float]): The value to convert.

    Returns:
        float: The converted float value.

    Raises:
        ValueError: If the value cannot be converted to float.
    """
    if isinstance(x, str):
        return round(float(x.replace("<", "").strip()), 3)
    return x


def string_test(value: Union[str, float]) -> Optional[str]:
    """
    Checks if a value can be converted to float.

    Args:
        value (Union[str, float]): The value to test.

    Returns:
        Optional[str]: The original value if it cannot be converted to float, None otherwise.
    """
    try:
        if isinstance(value, str) and '<' in value:
            float(value.replace('<', '').strip())
        else:
            float(value)
        return None
    except ValueError:
        return value
    except TypeError:
        return None


def get_columns_with_incorrect_values(df: pd.DataFrame) -> bool:
    """
    Finds columns in a DataFrame that contain incorrect values that can't be converted to float.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        bool: True if columns with incorrect values are found, False otherwise.
    """
    # Skip the first two columns (typically metadata columns like well and date)
    if len(df.columns) <= 2:
        return False
        
    str_cols = df.select_dtypes(object).columns[2:]
    
    # Apply string_test to each column and collect columns with invalid values
    invalid_columns = []
    for col in str_cols:
        invalid_values = df[col].apply(string_test).dropna()
        if len(invalid_values) > 0:
            print(f"Column name: {col}\nValues: {invalid_values.values}\n")
            invalid_columns.append(invalid_values)
            
    return len(invalid_columns) > 0