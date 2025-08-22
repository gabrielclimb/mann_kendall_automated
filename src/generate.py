
from typing import Tuple

import pandas as pd

from .utils.fix_string import get_columns_with_incorrect_values, string_to_float
from .utils.mann_kendall import mk_test
from .utils.progress_bar import print_progress_bar


def transpose_dataframe(file_name: str) -> pd.DataFrame:
    """
    Transposes the given DataFrame, replaces "ND" with 0.5, and renames columns.

    Args:
        file_name (str): Name of the file containing the DataFrame.

    Returns:
        pd.DataFrame: Transposed DataFrame with modified columns.
    """
    df = pd.read_excel(file_name, header=None, index_col=0)
    df = df.replace("ND", 0.5)
    df_tranposto = df.T
    df_tranposto.columns.values[0] = "well"
    df_tranposto.columns.values[1] = "Date"
    return df_tranposto


def generate_mann_kendall(file_name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates the Mann Kendall test results and transposed DataFrame.

    Args:
        file_name (str): Name of the file containing the DataFrame.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Tuple containing the results
            DataFrame and the transposed DataFrame.
    """

    df_tranposto = transpose_dataframe(file_name)

    if get_columns_with_incorrect_values(df_tranposto):
        print("You should fix this values firts")
        raise TypeError

    # check the number of samples per well, if less than 5, its ignore.

    wells = pd.DataFrame(df_tranposto.well.value_counts() > 4).reset_index()
    wells.columns = ["index", "well"]

    wells = wells[wells.well].iloc[:, 0]

    colunas = df_tranposto.columns[2:]

    results = pd.DataFrame()
    array = []
    print_progress_bar(0, len(wells), prefix="Progress:", suffix="Complete", length=50)
    count = 0
    for w in wells:
        count += 1
        print_progress_bar(
            count, len(wells), prefix="Progress:", suffix="Complete", length=50
        )
        df_temp = df_tranposto[df_tranposto.well == w]
        for c in colunas:
            try:
                if df_temp.loc[:, c].dropna().count() > 3:
                    valores = df_temp.loc[:, c].apply(string_to_float).dropna().values
                    trend, s, cv, cf = mk_test(valores)
                    array = [w, c, trend, s, cv, cf]
                    results = pd.concat(
                        [results, pd.DataFrame([array])], ignore_index=True
                    )
                else:
                    continue
            except TypeError:
                valores = df_temp.loc[:, c].apply(string_to_float).fillna(0).values
                raise TypeError(f"incorrect values: {valores}")

    results.columns = [
        "Well",
        "Analise",
        "Trend",
        "Mann-Kendall Statistic (S)",
        "Coefficient of Variation",
        "Confidence Factor",
    ]
    return results, df_tranposto


# def generate_xlsx(file_name):
#     today = datetime.today().strftime("%Y_%m_%d")
#     random_number = randint(1000, 5000)
#     new_name = file_name.split("/")[-1].split('.')[0]
#     output_name = f"output_tables/{new_name}_{today}_{random_number}.xlsx"
#     try:
#         results = generate_mann_kendall(file_name)
#     except TypeError:
#         exit()
#     results.to_excel(output_name, index=False, sheet_name="mann_kendall")
