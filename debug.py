
from __future__ import division

import os
import glob
import pandas as pd
from datetime import datetime

from mann_kendall_automated.utils.mann_kendall import mk_test
from mann_kendall_automated.utils.fix_string import string_to_float,\
    string_test


# nao alterar esse arquivo de entrada
KENDALL_DIST = pd.read_csv(
    "mann_kendall_automated/utils/file/kendall_dist.csv",
    index_col=0,
    sep=";")

file = glob.glob(os.getcwd() + "/input_tables" + "/*.xlsx")

df = pd.read_excel(file[1], header=None, index_col=0)
df = df.replace("ND", 0.5)
df_tranposto = df.T
df_tranposto.columns.values[0] = "well"
df_tranposto.columns.values[1] = "Date"

str_cols = df_tranposto.select_dtypes(object).columns[1:]

string_in_float = [df for df in [df_tranposto[col].apply(string_test).dropna()
                                 for col in str_cols] if len(df) > 0]

if len(string_in_float):
    for s in string_in_float:
        print(f'Column name: {s.name}\nValues: {s.values}\n')


# checa o numero de amostras por poço, se for menos do que 4 é ignorado.
wells = pd.DataFrame(df_tranposto.well.value_counts() > 4).reset_index()

wells = wells[wells.well == True].iloc[:, 0]

colunas = df_tranposto.columns[2:]


results = pd.DataFrame()
array = []
for w in wells:
    df_temp = df_tranposto[df_tranposto.well == w]
    print(w)
    for c in colunas:
        print(c)

        try:
            valores = df_temp.loc[:, c].apply(string_to_float).fillna(0).values
            trend, s, cv, cf = mk_test(valores, KENDALL_DIST)
            array = [w, c, trend, s, cv, cf]
            print(array)
            results = results.append([array], ignore_index=True)
        except TypeError:
            raise TypeError(f'incorrect values: {valores}')

results.columns = ['Well', 'Analise', 'Trend',
                   "Mann-Kendall Statistic (S)",
                   'Coefficient of Variation',
                   'Confidence Factor']

today = datetime.today().strftime("%Y_%m_%d")
output_name = f"output_tables/Mann_Kendall_{today}.xlsx"

results.to_excel(output_name, index=False, sheet_name="mann_kendall")

