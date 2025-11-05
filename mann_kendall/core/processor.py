from typing import Tuple

import numpy as np
import pandas as pd

from mann_kendall.core.constants import (
    MIN_SAMPLES_FOR_ANALYSIS,
    MIN_SAMPLES_PER_COMPONENT,
    NOT_DETECTED_MARKERS,
    NOT_DETECTED_VALUE,
)
from mann_kendall.core.mann_kendall import mk_test
from mann_kendall.data.cleaner import get_columns_with_incorrect_values, string_to_float
from mann_kendall.utils.logging_config import get_logger
from mann_kendall.utils.progress import print_progress_bar

logger = get_logger(__name__)


def transpose_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transposes the given DataFrame, handles "ND" (not detected) values, 
    and renames columns for further processing.

    Args:
        df (pd.DataFrame): Input DataFrame to transpose. Expected to have wells as columns,
                          with dates and components as rows.

    Returns:
        pd.DataFrame: Transposed DataFrame with columns renamed and standardized:
                     - 'well': contains well names
                     - 'Date': contains date information
                     - Additional columns contain component values

    Notes:
        - "ND", "N/D", and other not-detected indicators will be replaced with 0.5
        - Empty cells will be preserved as NaN for proper handling
    """
    # Handle common not-detected indicators
    df = df.replace(list(NOT_DETECTED_MARKERS) + ["<ND"], NOT_DETECTED_VALUE)
    
    # Transpose the DataFrame (columns become rows)
    df_transposto = df.T
    
    # Rename the first two columns for standardization
    if len(df_transposto.columns) >= 2:
        df_transposto.columns.values[0] = "well"
        df_transposto.columns.values[1] = "Date"
    else:
        raise ValueError(
            "DataFrame must have at least two columns after transposition. "
            "Expected format: First column should contain dates, subsequent columns should contain well data."
        )
    
    # Convert date columns to datetime where possible
    try:
        df_transposto["Date"] = pd.to_datetime(df_transposto["Date"])
    except Exception as e:
        # If conversion fails, keep as is - might be a custom date format
        logger.warning("Could not convert dates to datetime format: %s", str(e))
        
    return df_transposto


def process_well_data(well_name: str, df_transposto: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Process data for a specific well and runs Mann-Kendall test for each component.

    Args:
        well_name (str): Name of the well to process
        df_transposto (pd.DataFrame): Transposed data containing all wells
        columns (list): List of columns (components) to analyze

    Returns:
        pd.DataFrame: Results of Mann-Kendall tests for this well
        
    Raises:
        TypeError: If values can't be converted to float
        ValueError: If insufficient data points after filtering NaN values
        ZeroDivisionError: If mean of data is zero (can't calculate coefficient of variation)
    """
    results = pd.DataFrame()
    df_temp = df_transposto[df_transposto.well == well_name]

    for column in columns:
        try:
            # Check if we have enough data points after removing NaNs
            filtered_data = df_temp.loc[:, column].dropna()
            if filtered_data.count() >= MIN_SAMPLES_PER_COMPONENT:
                # Convert values and drop any remaining NaNs
                values = filtered_data.apply(string_to_float).dropna().values
                
                # Check for all zeros which would cause division by zero in CV calculation
                if np.mean(values) == 0:
                    continue
                    
                result = mk_test(values)
                array = [well_name, column, result.trend, result.statistic, 
                         result.coefficient_of_variation, result.confidence_factor]
                results = pd.concat([results, pd.DataFrame([array])], ignore_index=True)
            # else: silently skip components with insufficient data
        except TypeError as e:
            values = df_temp.loc[:, column].apply(string_to_float).fillna(0).values
            raise TypeError(
                f"Incorrect values in well '{well_name}', column '{column}': {values}. "
                f"Please ensure all values are numeric or recognized markers (ND, N/D, etc.). Error: {e}"
            )
        except ZeroDivisionError:
            # This could happen if all values are zero (CV calculation would fail)
            raise ValueError(
                f"Cannot calculate trend for well '{well_name}', component '{column}': "
                f"All values are zero or not detected. No trend can be calculated."
            )

    return results


def generate_mann_kendall(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processes input data and generates Mann-Kendall test results for all wells.

    Args:
        df (pd.DataFrame): Input DataFrame with time series data

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Results DataFrame and the transposed DataFrame
    """
    df_transposto = transpose_dataframe(df)

    if get_columns_with_incorrect_values(df_transposto):
        error_msg = (
            "Input data contains values that cannot be converted to float. "
            "Please check the error messages above for specific columns and values. "
            "Acceptable formats: numeric values, 'ND', 'N/D', 'NOT DETECTED', or values with '<' prefix."
        )
        logger.error(error_msg)
        raise TypeError(error_msg)

    # Check the number of samples per well
    wells = pd.DataFrame(
        df_transposto.well.value_counts() >= MIN_SAMPLES_FOR_ANALYSIS
    ).reset_index()
    wells.columns = ["index", "well"]
    wells = wells[wells.well].iloc[:, 0]

    total_wells = len(df_transposto.well.unique())
    filtered_wells = len(wells)
    if filtered_wells < total_wells:
        logger.info(
            "Filtered wells: %d out of %d wells have at least %d samples and will be analyzed",
            filtered_wells, total_wells, MIN_SAMPLES_FOR_ANALYSIS
        )

    columns = df_transposto.columns[2:]

    results = pd.DataFrame()
    logger.info("Starting analysis of %d wells with %d components", len(wells), len(columns))
    print_progress_bar(0, len(wells), prefix="Processing wells:", suffix="Complete", length=50)

    for i, well in enumerate(wells):
        print_progress_bar(
            i + 1, len(wells), prefix="Processing wells:", suffix="Complete", length=50
        )
        logger.debug("Processing well: %s (%d/%d)", well, i + 1, len(wells))
        well_results = process_well_data(well, df_transposto, columns)
        results = pd.concat([results, well_results], ignore_index=True)

    results.columns = [
        "Well",
        "Analise",
        "Trend",
        "Mann-Kendall Statistic (S)",
        "Coefficient of Variation",
        "Confidence Factor",
    ]

    return results, df_transposto
