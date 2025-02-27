from typing import Tuple

import pandas as pd

from mann_kendall.core.mann_kendall import mk_test
from mann_kendall.data.cleaner import get_columns_with_incorrect_values, string_to_float
from mann_kendall.utils.progress import print_progress_bar


def transpose_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transposes the given DataFrame, replaces "ND" with 0.5, and renames columns.

    Args:
        df (pd.DataFrame): Input DataFrame to transpose

    Returns:
        pd.DataFrame: Transposed DataFrame with modified columns
    """
    df = df.replace("ND", 0.5)
    df_transposto = df.T
    df_transposto.columns.values[0] = "well"
    df_transposto.columns.values[1] = "Date"
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
    """
    results = pd.DataFrame()
    df_temp = df_transposto[df_transposto.well == well_name]

    for column in columns:
        try:
            if df_temp.loc[:, column].dropna().count() > 3:
                values = df_temp.loc[:, column].apply(string_to_float).dropna().values
                trend, s, cv, cf = mk_test(values)
                array = [well_name, column, trend, s, cv, cf]
                results = pd.concat([results, pd.DataFrame([array])], ignore_index=True)
        except TypeError:
            values = df_temp.loc[:, column].apply(string_to_float).fillna(0).values
            raise TypeError(f"incorrect values: {values}")

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
