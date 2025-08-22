from typing import Tuple

import numpy as np
import pandas as pd

from mann_kendall.core.mann_kendall import mk_test
from mann_kendall.data.cleaner import get_columns_with_incorrect_values, string_to_float
from mann_kendall.utils.progress import print_progress_bar


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
    df = df.replace(["ND", "N/D", "NOT DETECTED", "<ND"], 0.5)
    
    # Transpose the DataFrame (columns become rows)
    df_transposto = df.T
    
    # Rename the first two columns for standardization
    if len(df_transposto.columns) >= 2:
        df_transposto.columns.values[0] = "well"
        df_transposto.columns.values[1] = "Date"
    else:
        raise ValueError("DataFrame must have at least two columns after transposition")
    
    # Convert date columns to datetime where possible
    try:
        df_transposto["Date"] = pd.to_datetime(df_transposto["Date"])
    except Exception:
        # If conversion fails, keep as is - might be a custom date format
        pass
        
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
            # Check if we have enough data points (at least 4) after removing NaNs
            filtered_data = df_temp.loc[:, column].dropna()
            if filtered_data.count() > 3:
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
        except TypeError:
            values = df_temp.loc[:, column].apply(string_to_float).fillna(0).values
            raise TypeError(f"Incorrect values in column {column}: {values}")
        except ZeroDivisionError:
            # This could happen if all values are zero (CV calculation would fail)
            raise ValueError(f"Cannot calculate trend for {column}: All values are zero")

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
        print("You should fix these values first")
        raise TypeError("Input data contains string values that cannot be converted to float")

    # Check the number of samples per well, if less than 5, it's ignored
    wells = pd.DataFrame(df_transposto.well.value_counts() > 4).reset_index()
    wells.columns = ["index", "well"]
    wells = wells[wells.well].iloc[:, 0]

    columns = df_transposto.columns[2:]

    results = pd.DataFrame()
    print_progress_bar(0, len(wells), prefix="Processing wells:", suffix="Complete", length=50)

    for i, well in enumerate(wells):
        print_progress_bar(
            i + 1, len(wells), prefix="Processing wells:", suffix="Complete", length=50
        )
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
