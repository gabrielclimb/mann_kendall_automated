#!/usr/bin/env python

"""Tests for the data loader module."""

import os
from pathlib import Path

import pandas as pd
import pytest

from mann_kendall.data.loader import load_excel_data, validate_input_format

# Get the path to the test files
TEST_FILES_DIR = Path(__file__).parent.parent / "files"


def test_load_excel_data_path():
    """Test loading Excel data from file path."""
    file_path = os.path.join(TEST_FILES_DIR, "example_input.xlsx")
    df = load_excel_data(file_path)
    
    assert isinstance(df, pd.DataFrame)
    assert df.shape[1] > 0  # Should have at least one column
    assert not df.empty


def test_load_excel_invalid_file():
    """Test loading Excel data from an invalid file."""
    with pytest.raises(FileNotFoundError):  # Or the specific exception type that should be raised
        load_excel_data("non_existent_file.xlsx")


def test_validate_input_format_valid():
    """Test validating a correctly formatted input DataFrame."""
    # Create a valid DataFrame
    df = pd.DataFrame({
        "Well1": [1.0, 2.0],
        "Well2": [3.0, 4.0]
    }, index=["2020-01-01", "Component"])
    
    # Should not raise an exception
    assert validate_input_format(df)


def test_validate_input_format_too_few_columns():
    """Test validating a DataFrame with too few columns."""
    # Create a DataFrame with only one column
    df = pd.DataFrame({
        "Well1": [1.0, 2.0]
    }, index=["2020-01-01", "Component"])
    
    with pytest.raises(ValueError):
        validate_input_format(df)