from typing import Optional, Union

import pandas as pd


def string_to_float(x: Union[str, float]) -> float:
    """
    Converts a string representation of a number to a float.
    Handles special cases like "<0.01" by removing the "<" symbol.
    Also handles 'ND' (Not Detected) or empty strings.

    Args:
        x (Union[str, float]): The value to convert.

    Returns:
        float: The converted float value.

    Raises:
        ValueError: If the value cannot be converted to float.
    """
    if x is None:
        return float('nan')
        
    if isinstance(x, str):
        x = x.strip()
        # Handle empty string
        if not x:
            return float('nan')
        # Handle Not Detected values (could be represented in different ways)
        if x.upper() in ('ND', 'N/D', 'NOT DETECTED'):
            return 0.5  # Default replacement for not detected values
        # Handle values with < prefix (e.g., "<0.01")
        if '<' in x:
            return round(float(x.replace("<", "").strip()), 3)
        try:
            # Handle normal string numbers
            return float(x)
        except ValueError:
            raise ValueError(f"Cannot convert '{x}' to float")
            
    return float(x)  # Handle numerical values or numpy types


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
    Also returns a more informative report about which columns and values are problematic.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        bool: True if columns with incorrect values are found, False otherwise.
    """
    # Skip the first two columns (typically metadata columns like well and date)
    if len(df.columns) <= 2:
        return False
        
    # Find columns with string (object) data type, skipping metadata columns
    str_cols = df.select_dtypes(object).columns[2:]
    
    # Apply string_test to each column and collect columns with invalid values
    invalid_columns = []
    issues_report = []
    
    for col in str_cols:
        invalid_values = df[col].apply(string_test).dropna()
        if len(invalid_values) > 0:
            invalid_columns.append(col)
            issues_report.append({
                "column": col,
                "invalid_values": invalid_values.values.tolist(),
                "counts": len(invalid_values)
            })
            print(f"Column name: {col}\nValues: {invalid_values.values}\nCount: {len(invalid_values)}\n")
            
    # Format the report in a more readable way
    if issues_report:
        print("\nSummary of data issues:")
        print(f"Found {len(invalid_columns)} columns with invalid values")
        for issue in issues_report:
            print(f"- Column '{issue['column']}': {issue['counts']} invalid values")
    
    return len(invalid_columns) > 0