import pytest

from .context import string_test, string_to_float


def test_string_to_float():
    value = "< 2"
    string = 'test<'
    assert 2 == string_to_float(value)
    assert type(string_to_float(value)) == float
    with pytest.raises(ValueError):
        string_to_float(string)


def test_string_to_test():
    value = "2"
    string = 'test'
    assert None == string_test(value)
    assert 'test' == string_test(string)
