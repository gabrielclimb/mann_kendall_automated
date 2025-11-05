from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Union

import pandas as pd

from mann_kendall.core.constants import (
    MAX_FILE_SIZE_BYTES,
    MIN_POINTS_FOR_RELIABLE_TEST,
    MIN_SAMPLES_PER_COMPONENT,
    SUPPORTED_FILE_EXTENSIONS,
)
from mann_kendall.utils.logging_config import get_logger

logger = get_logger(__name__)


# noqa: E501
def load_excel_data(
    file_content: Union[str, bytes, BinaryIO],
    max_size: int = MAX_FILE_SIZE_BYTES
) -> pd.DataFrame:
    """
    Loads data from an Excel file into a pandas DataFrame and validates its format.

    Args:
        file_content (Union[str, bytes, BinaryIO]):
            Either a file path string, bytes object containing Excel data,
            or a file-like object.
        max_size: Maximum allowed file size in bytes (default: 10MB)

    Returns:
        pd.DataFrame: DataFrame containing the loaded data with index_col=0 and no header

    Raises:
        pd.errors.EmptyDataError: If the file is empty
        pd.errors.ParserError: If the file cannot be parsed as an Excel file
        ValueError: If the file format is invalid or file is too large
        FileNotFoundError: If the file doesn't exist (when path is provided)

    Examples:
        >>> df = load_excel_data("path/to/file.xlsx")
        >>> df = load_excel_data(file_bytes)
    """
    try:
        # Validate file extension if path is provided
        if isinstance(file_content, str):
            file_path = Path(file_content)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_content}")
            if file_path.suffix.lower() not in SUPPORTED_FILE_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file type: {file_path.suffix}. "
                    f"Supported formats: {', '.join(SUPPORTED_FILE_EXTENSIONS)}"
                )
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > max_size:
                raise ValueError(
                    f"File too large: {file_size:,} bytes (max: {max_size:,} bytes / "
                    f"{max_size / (1024 * 1024):.1f} MB)"
                )
            logger.info("Loading Excel file: %s (Size: %d bytes)", file_content, file_size)

        if isinstance(file_content, bytes):
            # Check byte content size
            if len(file_content) > max_size:
                raise ValueError(
                    f"File too large: {len(file_content):,} bytes (max: {max_size:,} bytes / "
                    f"{max_size / (1024 * 1024):.1f} MB)"
                )
            logger.info("Loading Excel file from bytes (Size: %d bytes)", len(file_content))
            file_content = BytesIO(file_content)

        # Check file-like object size if it has a size attribute
        if hasattr(file_content, 'size') and file_content.size > max_size:
            raise ValueError(
                f"File too large: {file_content.size:,} bytes (max: {max_size:,} bytes)"
            )

        df = pd.read_excel(file_content, header=None, index_col=0, engine="openpyxl")
        validate_input_format(df)
        return df
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The uploaded file is empty. Please provide a file with data.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Unable to parse the file. Please ensure it's a valid Excel file.")
    except ValueError as e:
        raise ValueError(f"Invalid file format: {str(e)}")
    except Exception as e:
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
    if df.empty:
        raise pd.errors.EmptyDataError("Input DataFrame is empty")

    if df.shape[1] < 2:
        raise ValueError("Input file must have at least two columns (date and one well)")

    if len(df.index) < 2:
        raise ValueError("Input file must have at least two rows (date and component)")

    has_date_format = False

    try:
        if isinstance(df.index[0], str):
            pd.to_datetime(df.index[: min(5, len(df.index))])
            has_date_format = True
    except (ValueError, TypeError):
        pass

    if not has_date_format and not isinstance(df.index[0], pd.Timestamp) and not pd.isna(df.index[0]):
        raise ValueError("First column must contain valid dates or date-like strings")

    if df.columns.isna().any():
        raise ValueError("Well names (column headers) cannot be empty")

    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicate well names found. Each well must have a unique name.")

    if df.iloc[0].isna().all():
        raise ValueError("Component names (second row) cannot be all empty")

    return True

# noqa: E501
def check_data_sufficiency(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Check if the data has sufficient points for reliable Mann-Kendall analysis.

    Args:
        df: The loaded DataFrame

    Returns:
        Tuple of (is_sufficient, warning_message)
    """
    if len(df.index) < MIN_SAMPLES_PER_COMPONENT:
        return (
            False,
            f"""Your data has only {len(df.index)} time points.
            Mann-Kendall test requires at least {MIN_SAMPLES_PER_COMPONENT} data points.""",
        )
    elif len(df.index) < MIN_POINTS_FOR_RELIABLE_TEST:
        return (
            True,
            f"Your data has {len(df.index)} time points. Consider adding more data points "
            f"for more reliable trend detection (recommended: {MIN_POINTS_FOR_RELIABLE_TEST}+).",
        )

    return True, ""
