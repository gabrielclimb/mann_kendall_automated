import pytest
from .context import generate_mann_kendall


class TestGenerateMannKendall:

    file = 'mann_kendall_automated/tests/files/example_input.xlsx'
    result = generate_mann_kendall(file)

    def test_size(self):
        assert len(self.result) == 146

    def test_columns_order(self):
        columns = ['Well', 'Analise', 'Trend',
                   'Mann-Kendall Statistic (S)',
                   'Coefficient of Variation', 'Confidence Factor']
        for i in range(len(columns)):
            assert self.result.columns[i] == columns[i]
    
