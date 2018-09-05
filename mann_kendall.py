
from __future__ import division
import numpy as np
import pandas as pd
from datetime import datetime
import glob
import os

from scipy.stats import norm


def mk_test(x, kendall_dist, alpha=0.05):
    """
    This function is derived from code originally posted by Sat Kumar Tomer
    (satkumartomer@gmail.com)
    See also: http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
    The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
    1987) is to statistically assess if there is a monotonic upward or downward
    trend of the variable of interest over time. A monotonic upward (downward)
    trend means that the variable consistently increases (decreases) through
    time, but the trend may or may not be linear. The MK test can be used in
    place of a parametric linear regression analysis, which can be used to test
    if the slope of the estimated linear regression line is different from
    zero. The regression analysis requires that the residuals from the fitted
    regression line be normally distributed; an assumption not required by the
    MK test, that is, the MK test is a non-parametric (distribution-free) test.
    Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
    viewed as an exploratory analysis and is most appropriately used to
    identify stations where changes are significant or of large magnitude and
    to quantify these findings.
    Input:
        x:   a vector of data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p value of the significance test
        z: normalized test statistics
    Examples
    --------
      >>> x = np.random.rand(100)
      >>> trend,h,p,z = mk_test(x,0.05)
    """
    n = len(x)

    # calculate S
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])

    # calculate the unique data
    unique_x = np.unique(x)
    g = len(unique_x)

    # calculate the var(s)
    if n == g:  # there is no tie
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else:  # there are some ties in data
        tp = np.zeros(unique_x.shape)
        for i in range(len(unique_x)):
            tp[i] = sum(x == unique_x[i])
        var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:  # s == 0:
        z = 0

    # ----------------
    # Arcadis section
    # ----------------
    # Coefficient of Variation
    cv = np.std(x, ddof=1) / np.mean(x)

    # ----------------
    # Confidence Factor
    ken_LINHA = int(abs(s))  # COLUNA
    ken_COLUNA = len(x) - 4  # LINHA
    cf = 1 - float(kendall_dist.iloc[ken_LINHA, ken_COLUNA])
    # ----------------

    # calculate the p_value
    p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
    h = abs(z) > norm.ppf(1 - alpha / 2)

    if cf < 0.9:
        if s <= 0 and cv < 1:
            trend = "Stable"
        else:
            trend = 'No Trend'
    else:
        if cf <= 0.95:
            if s > 0:
                trend = "Prob. Increasing"
            else:
                trend = "Prob. Decreasing"
        else:
            if s > 0:
                trend = "Increasing"
            else:
                trend = "Decreasing"

    return trend, round(s, 4), round(cv, 2), round(cf, 3)


def gera_xlsx(file_name):

    # nao alterar esse arquivo de entrada
    kendall_dist = pd.read_csv("kendall_dist.csv", index_col=0, sep=";")

    df = pd.read_excel(file_name, header=None, index_col=None)
    df = df.replace("ND", 0.5)
    df2 = df.T
    df2 = df2.rename(columns=df2.iloc[0])
    df2 = df2.drop(0, axis=0)
    df2.columns.values[0] = "well"
    df2.columns.values[1] = "Date"

    # checa o numero de amostras por poço, se for menos do que 4 é ignorado.
    wells = pd.DataFrame(df2.well.value_counts() > 4).reset_index()

    # df2 = df2.set_index("well")

    wells = wells[wells.well == True].iloc[:, 0]

    colunas = df2.columns[2:]

    df2 = df2.replace("<", "")

    results = pd.DataFrame()
    array = []
    for w in wells:
        df_temp = df2[df2.well == w]
        print(w)
        for c in colunas:
            print(c)
            valores = df_temp.loc[:, c].fillna(0).values
            trend, s, cv, cf = mk_test(valores, kendall_dist)
            array = [w, c, trend, s, cv, cf]
            print(array)
            results = results.append([array], ignore_index=True)

    results.columns = ['Well', 'Analise', 'Trend', "Mann-Kendall Statistic (S)",
                       'Coefficient of Variation', 'Confidence Factor']

    today = datetime.today().strftime("%Y_%m_%d")
    output_name = f"Mann_Kendall_{today}.xlsx"

    results.to_excel(output_name, index=False, sheet_name="mann_kendall")


def main():

    file = glob.glob(os.getcwd() + "/*.xlsx")
    x = 0
    while x != "sair":
        count = 0
        for f in file:
            print(f"{count}: Arquivo {f}")
            count += 1

        x = input(f"Escollha um arquivo pelo numero ou digite sair.\n")
        if x.isdigit():
            gera_xlsx(file[int(x)])
        else:
            x = "sair"


if __name__ == '__main__':
    main()
