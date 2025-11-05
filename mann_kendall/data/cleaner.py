from typing import Optional, Union

import pandas as pd

from mann_kendall.core.constants import NOT_DETECTED_MARKERS, NOT_DETECTED_VALUE
from mann_kendall.utils.logging_config import get_logger

logger = get_logger(__name__)


def string_to_float(x: Union[str, float]) -> float:
    """
    Converts string values to float with special handling for environmental data markers.

    This function is designed specifically for environmental monitoring data where values
    may contain special markers for non-detected or below-detection-limit measurements.

    Args:
        x: The value to convert. Can be:
           - Numeric string: "12.5", "0.01"
           - Below detection limit: "<0.01", "<5"
           - Not detected markers: "ND", "N/D", "NOT DETECTED"
           - Empty string: "" (converted to NaN)
           - Already numeric: int or float

    Returns:
        float: Converted numeric value. Special cases:
            - Not detected markers → 0.5 (configurable via constants)
            - Empty strings → NaN
            - "<value" → value (detection limit used)

    Raises:
        ValueError: If the string cannot be converted to a valid float.

    Examples:
        >>> string_to_float("12.5")
        12.5
        >>> string_to_float("ND")
        0.5
        >>> string_to_float("<0.01")
        0.01
        >>> string_to_float("")
        nan
    """
    if x is None:
        return float('nan')
        
    if isinstance(x, str):
        x = x.strip()
        # Handle empty string
        if not x:
            return float('nan')
        # Handle Not Detected values (could be represented in different ways)
        if x.upper() in NOT_DETECTED_MARKERS:
            return NOT_DETECTED_VALUE  # Default replacement for not detected values
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
    Tests whether a value can be successfully converted to float.

    This is a validation function used to identify problematic data values
    before processing. It handles the same special cases as string_to_float.

    Args:
        value: The value to test (string or numeric type)

    Returns:
        The original value if it cannot be converted to float (indicating an error),
        None if the conversion would succeed.

    Examples:
        >>> string_test("12.5")
        None  # Can be converted
        >>> string_test("ND")
        None  # Can be converted (handled as special case)
        >>> string_test("invalid")
        'invalid'  # Cannot be converted
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
    Validates DataFrame columns and identifies values that cannot be converted to float.

    This function scans all data columns (excluding the first two metadata columns
    which typically contain well names and dates) and reports any values that
    cannot be converted to numeric format using string_to_float.

    Logging:
        - Warnings are logged for each column with invalid values
        - A summary report is logged showing all problematic columns

    Args:
        df: The DataFrame to validate. Expected to have:
           - Column 0: Well names (metadata, not validated)
           - Column 1: Dates (metadata, not validated)
           - Columns 2+: Numeric data to validate

    Returns:
        True if any columns contain unconvertible values, False if all data is valid.

    Examples:
        >>> df = pd.DataFrame({
        ...     'well': ['A', 'A'],
        ...     'Date': ['2024-01-01', '2024-01-02'],
        ...     'pH': ['7.2', 'invalid']
        ... })
        >>> get_columns_with_incorrect_values(df)
        # Logs warning about 'pH' column
        True
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
            logger.warning(
                "Column '%s' contains invalid values: %s (Count: %d)",
                col, invalid_values.values, len(invalid_values)
            )

    # Format the report in a more readable way
    if issues_report:
        logger.warning("Summary of data issues:")
        logger.warning("Found %d columns with invalid values", len(invalid_columns))
        for issue in issues_report:
            logger.warning("- Column '%s': %d invalid values", issue['column'], issue['counts'])
    
    return len(invalid_columns) > 0