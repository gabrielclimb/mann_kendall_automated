#!/usr/bin/env python

"""
Pytest configuration file.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add the project root to sys.path to ensure modules can be imported in tests
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        "Well1": [1.0, 2.0, 3.0],
        "Well2": [4.0, 5.0, 6.0]
    }, index=["2020-01-01", "2020-02-01", "Component"])


@pytest.fixture
def sample_transposed_dataframe():
    """Create a sample transposed DataFrame for testing."""
    return pd.DataFrame({
        "well": ["Well1", "Well2", "Well3"],
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "Component1": [1.0, 2.0, 3.0],
        "Component2": [4.0, 5.0, 6.0]
    })


@pytest.fixture
def increasing_data():
    """Create sample data with increasing trend."""
    return np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


@pytest.fixture
def decreasing_data():
    """Create sample data with decreasing trend."""
    return np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])


@pytest.fixture
def no_trend_data():
    """Create sample data with no trend."""
    np.random.seed(42)  # For reproducibility
    return np.random.normal(size=20)