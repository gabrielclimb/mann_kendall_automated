#!/usr/bin/env python

"""Tests for the data cleaner module."""

import pandas as pd
import pytest

from mann_kendall.data.cleaner import (
    get_columns_with_incorrect_values,
    string_test,
    string_to_float,
)


def test_string_to_float_numeric():
    """Test string_to_float with numeric values."""
    assert string_to_float(5.0) == 5.0
    assert string_to_float("5.0") == 5.0
    assert string_to_float("5") == 5.0


def test_string_to_float_with_less_than():
    """Test string_to_float with strings containing '<'."""
    assert string_to_float("<0.01") == 0.01
    assert string_to_float("< 0.01") == 0.01
    assert string_to_float("<0.001") == 0.001


def test_string_to_float_rounding():
    """Test string_to_float rounding."""
    assert string_to_float("5.1234") == 5.123
    assert string_to_float("<0.01234") == 0.012


def test_string_to_float_exception():
    """Test string_to_float exception handling."""
    with pytest.raises(ValueError):
        string_to_float("not a number")


def test_string_test_valid():
    """Test string_test with valid numbers."""
    assert string_test(5.0) is None
    assert string_test("5.0") is None
    assert string_test("<0.01") is None


def test_string_test_invalid():
    """Test string_test with invalid numbers."""
    assert string_test("not a number") == "not a number"
    assert string_test("5.0a") == "5.0a"


def test_get_columns_with_incorrect_values_valid():
    """Test get_columns_with_incorrect_values with valid data."""
    # Create test DataFrame with all valid values
    df = pd.DataFrame({
        "well": ["Well1", "Well2", "Well3"],
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "Component1": ["5.0", "6.0", "7.0"],
        "Component2": ["<0.01", "0.02", "<0.005"]
    })
    
    assert not get_columns_with_incorrect_values(df)


def test_get_columns_with_incorrect_values_invalid():
    """Test get_columns_with_incorrect_values with invalid data."""
    # Create test DataFrame with some invalid values
    df = pd.DataFrame({
        "well": ["Well1", "Well2", "Well3"],
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "Component1": ["5.0", "invalid", "7.0"],
        "Component2": ["<0.01", "0.02", "<0.005"]
    })
    
    assert get_columns_with_incorrect_values(df)