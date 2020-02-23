import pytest

from .context import string_test, string_to_float,\
    get_columns_with_incorrect_values, transpose_dataframe


class TestFixString:
    PATH = 'mann_kendall_automated/tests/files/'
    file = PATH + 'example_input.xlsx'
    file_error = PATH + 'example_input_with_string.xlsx'
    df_error = transpose_dataframe(file_error)
    df_right = transpose_dataframe(file)
    value_right = "2"
    string_right = 'test'
    value_wrong = "< 2"
    string_wrong = 'test<'

    def test_string_to_float(self):
        assert 2 == string_to_float(self.value_wrong)
        assert type(string_to_float(self.value_wrong)) == float
        with pytest.raises(ValueError):
            string_to_float(self.string_wrong)

    def test_string_to_test(self):
        assert string_test(self.value_right) is None
        assert self.string_right == string_test(self.string_right)

    def test_get_columns_with_incorrect_values(self):
        assert get_columns_with_incorrect_values(self.df_error)

    def test_get_columns_with_right_values(self):
        assert get_columns_with_incorrect_values(self.df_right) is None


