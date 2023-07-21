from typing import Optional, Union

import pandas as pd


def string_to_float(x: Union[str, float]) -> float:
    """
    Converts a string representation of a number to a float.

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


def string_test(value: Union[str, float]):
    """
    Checks if a value can be converted to float.

    Args:
        value (Union[str, float]): The value to test.

    Returns:
        Optional[str]: The original value if it cannot be converted to float,
                       None otherwise.
    """
    try:
        float(value)
    except ValueError:
        return value
    except TypeError:
        pass


def get_columns_with_incorrect_values(df: pd.DataFrame) -> Optional[bool]:
    """
    Finds columns in a DataFrame that contain incorrect values.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        bool: True if columns with incorrect values are found, False otherwise.
    """
    str_cols = df.select_dtypes(object).columns[2:]
    string_in_float = [
        column
        for column in [df[col].apply(string_test).dropna() for col in str_cols]
        if len(column) > 0
    ]
    if len(string_in_float):
        for s in string_in_float:
            print(f"Column name: {s.name}\nValues: {s.values}\n")
        return True
