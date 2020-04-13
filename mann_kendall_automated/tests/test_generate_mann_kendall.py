import pytest
import pandas as pd
from .context import generate_mann_kendall, transpose_dataframe


file = 'mann_kendall_automated/tests/files/example_input.xlsx'


class TestGenerateMannKendall:

    result = generate_mann_kendall(file)

    def test_size(self):
        assert len(self.result) == 146

    def test_columns_order(self):
        columns = ['Well', 'Analise', 'Trend',
                   'Mann-Kendall Statistic (S)',
                   'Coefficient of Variation', 'Confidence Factor']
        for i in range(len(columns)):
            assert self.result.columns[i] == columns[i]


def test_transpose_dataframe():
    df_normal = pd.read_excel(file, header=None, index_col=0)
    df_tranposto = transpose_dataframe(file)
    assert df_normal.shape[0] == df_tranposto.shape[1]

