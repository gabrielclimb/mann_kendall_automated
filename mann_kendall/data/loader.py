from typing import BinaryIO, Union

import pandas as pd


def load_excel_data(file_content: Union[str, bytes, BinaryIO]) -> pd.DataFrame:
    """
    Loads data from an Excel file into a pandas DataFrame and validates its format.

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
        FileNotFoundError: If the file doesn't exist (when path is provided)
    """
    try:
        # Try to load the Excel file
        df = pd.read_excel(file_content, header=None, index_col=0)

        # Validate the format of the loaded data
        validate_input_format(df)

        return df
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(
            "The uploaded file is empty. Please provide a file with data."
        )
    except pd.errors.ParserError:
        raise pd.errors.ParserError(
            "Unable to parse the file. Please ensure it's a valid Excel file."
        )
    except ValueError as e:
        # Re-raise validation errors
        raise ValueError(f"Invalid file format: {str(e)}")
    except Exception as e:
        # Re-raise with more context for other errors
        raise type(e)(f"Error loading Excel file: {str(e)}")


def validate_input_format(df: pd.DataFrame) -> bool:
    """
    Validates that the input DataFrame has the expected format:
    - First row should be well names
    - First column should be dates
    - Second row should contain component names

    Args:
        df (pd.DataFrame): DataFrame to validate

    Returns:
        bool: True if valid, raises exception otherwise

    Raises:
        ValueError: If DataFrame does not have the expected format
        pd.errors.EmptyDataError: If DataFrame is empty
    """
    # Check if DataFrame is empty
    if df.empty:
        raise pd.errors.EmptyDataError("Input DataFrame is empty")

    # Check that DataFrame has minimum dimensions required
    if df.shape[1] < 2:
        raise ValueError("Input file must have at least two columns (date and one well)")

    if len(df.index) < 2:
        raise ValueError("Input file must have at least two rows (date and component)")

    # Check that first column (index) contains date-like values
    has_date_format = False

    # Try to convert first few index entries to datetime to validate date format
    try:
        if isinstance(df.index[0], str):
            pd.to_datetime(df.index[: min(5, len(df.index))])
            has_date_format = True
    except (ValueError, TypeError):
        pass

    if (
        not has_date_format
        and not isinstance(df.index[0], pd.Timestamp)
        and not pd.isna(df.index[0])
    ):
        raise ValueError("First column must contain valid dates or date-like strings")

    # Check for NaN in the first row (well names)
    if df.columns.isna().any():
        raise ValueError("Well names (column headers) cannot be empty")

    # Check for duplicate well names
    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicate well names found. Each well must have a unique name.")

    # Check that second row has values (component names)
    if df.iloc[0].isna().all():
        raise ValueError("Component names (second row) cannot be all empty")

    # Note: Mann-Kendall test works best with at least 4 data points
    # But we'll allow users to proceed with fewer points and show a warning

    return True


def check_data_sufficiency(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Check if the data has sufficient points for reliable Mann-Kendall analysis.

    Args:
        df: The loaded DataFrame

    Returns:
        Tuple of (is_sufficient, warning_message)
    """
    if len(df.index) < 4:
        return (
            False,
            f"Your data has only {len(df.index)} time points. Mann-Kendall test works best with at least 4 data points for reliable results.",
        )
    elif len(df.index) < 6:
        return (
            True,
            f"Your data has {len(df.index)} time points. Consider adding more data points for more reliable trend detection.",
        )

    return True, ""
