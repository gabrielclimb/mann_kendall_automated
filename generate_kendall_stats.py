
from __future__ import division

import os
from datetime import datetime
from random import randint

import glob
import pandas as pd

from utils.mann_kendall import mk_test
from utils.fix_string import string_to_float, get_columns_with_incorrect_values


def gera_xlsx(file_name):

    # keep it
    KENDALL_DIST = pd.read_csv("utils/kendall_dist.csv", index_col=0, sep=";")

    df = pd.read_excel(file_name, header=None, index_col=0)
    df = df.replace("ND", 0.5)
    df_tranposto = df.T
    df_tranposto.columns.values[0] = "well"
    df_tranposto.columns.values[1] = "Date"

    if get_columns_with_incorrect_values(df_tranposto):
        print('You should fix this values firts')
        exit()


    # check the number of samples per well, if less than 5, its ignore.
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
                valores = df_temp.loc[:, c].apply(
                    string_to_float).fillna(0).values
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
    output_name = f"output_tables/Mann_Kendall_{today}_{randint(1000, 5000)}.xlsx"

    results.to_excel(output_name, index=False, sheet_name="mann_kendall")


def main():

    file = glob.glob(os.getcwd() + "/input_tables" + "/*.xlsx")
    x = 0
    while x != "exit":
        count = 0
        for f in file:
            print(f"{count}: File {f}")
            count += 1

        x = input(f"Choose a file by number or type exit.\n")
        if x.isdigit():
            gera_xlsx(file[int(x)])
        else:
            x = "exit"


if __name__ == '__main__':
    main()
