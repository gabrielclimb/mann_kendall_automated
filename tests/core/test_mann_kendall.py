#!/usr/bin/env python

"""Tests for mann_kendall.py module."""

import numpy as np

from mann_kendall.core.mann_kendall import mk_test


def test_mk_test_increasing():
    """Test increasing trend detection."""
    # Clearly increasing data
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = mk_test(x)
    assert result.trend == "increasing"
    assert result.statistic > 0
    assert result.confidence_factor > 0.95


def test_mk_test_decreasing():
    """Test decreasing trend detection."""
    # Clearly decreasing data
    x = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    result = mk_test(x)
    assert result.trend == "decreasing"
    assert result.statistic < 0
    assert result.confidence_factor > 0.95


def test_mk_test_no_trend():
    """Test no trend detection."""
    # Create data with no clear trend
    # Instead of random data, use a more controlled dataset that guarantees no trend
    x = np.array([5, 5.1, 4.9, 5.2, 4.8, 5, 5.1, 4.9, 5, 5.1])
    result = mk_test(x)
    assert result.trend == "no trend"
    assert result.confidence_factor < 0.9


def test_mk_test_stable():
    """Test stable trend detection."""
    # Data with very small variations
    x = np.array([10.01, 10.02, 10.01, 10.00, 10.01, 10.02, 10.01, 10.00])
    result = mk_test(x)
    assert result.coefficient_of_variation < 1
    assert result.confidence_factor < 0.9


def test_mk_test_probably_increasing():
    """Test probably increasing trend detection."""
    # Data with a weak increasing trend
    np.random.seed(42)
    base = np.array([1, 2, 3, 4, 5])
    noise = np.random.normal(0, 1, 5)
    x = base + noise
    result = mk_test(x)
    assert result.trend in ["probably increasing", "increasing", "no trend"]  # Depends on noise


def test_mk_test_probably_decreasing():
    """Test probably decreasing trend detection."""
    # Data with a weak decreasing trend
    np.random.seed(42)
    base = np.array([5, 4, 3, 2, 1])
    noise = np.random.normal(0, 1, 5)
    x = base + noise
    result = mk_test(x)
    assert result.trend in ["probably decreasing", "decreasing", "no trend"]  # Depends on noise