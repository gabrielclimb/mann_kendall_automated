import os

from .context import generate_mann_kendall


class TestGenerateMannKendall:

    file = "src/tests/files/example_input.xlsx"
    print(os.listdir())
    result = generate_mann_kendall(file)

    def test_type(self):
        assert isinstance(self.result, tuple)

    def test_size(self):
        assert len(self.result[0]) == 146

    def test_columns_order(self):
        columns = [
            "Well",
            "Analise",
            "Trend",
            "Mann-Kendall Statistic (S)",
            "Coefficient of Variation",
            "Confidence Factor",
        ]
        for i, column in enumerate(columns):
            assert self.result[0].columns[i] == column
