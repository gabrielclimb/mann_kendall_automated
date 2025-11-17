"""
Caching utilities for Mann-Kendall calculations.

This module provides caching functionality to avoid redundant calculations
when processing identical datasets multiple times.
"""

from functools import lru_cache
from typing import Tuple

import numpy as np

from mann_kendall.core.mann_kendall import MKTestResult, mk_test
from mann_kendall.utils.logging_config import get_logger

logger = get_logger(__name__)


def _array_to_tuple(x: np.ndarray) -> Tuple[float, ...]:
    """
    Convert numpy array to tuple for hashability.

    Args:
        x: Numpy array to convert

    Returns:
        Tuple of array values
    """
    return tuple(x.tolist())


@lru_cache(maxsize=256)
def _mk_test_cached(
    data_tuple: Tuple[float, ...],
    alpha: float,
    seasonal: bool,
    period: int,
    calculate_slope: bool,
) -> MKTestResult:
    """
    Cached version of Mann-Kendall test.

    This function converts the tuple back to numpy array and calls mk_test.
    Results are cached using LRU cache to speed up repeated calculations
    on identical datasets.

    Args:
        data_tuple: Time series data as tuple (for hashability)
        alpha: Significance level
        seasonal: Whether to perform seasonal test
        period: Number of seasons
        calculate_slope: Whether to calculate Sen's slope

    Returns:
        MKTestResult with trend analysis results
    """
    data_array = np.array(data_tuple)
    return mk_test(data_array, alpha, seasonal, period, calculate_slope)


def mk_test_with_cache(
    x: np.ndarray,
    alpha: float = 0.05,
    seasonal: bool = False,
    period: int = 12,
    calculate_slope: bool = True,
    use_cache: bool = True,
) -> MKTestResult:
    """
    Mann-Kendall test with optional caching.

    This wrapper function provides caching for Mann-Kendall calculations,
    which can significantly speed up processing when analyzing similar
    datasets or reprocessing data.

    Args:
        x: Time series data
        alpha: Significance level (default: 0.05)
        seasonal: Whether to perform seasonal test (default: False)
        period: Number of seasons (default: 12)
        calculate_slope: Whether to calculate Sen's slope (default: True)
        use_cache: Whether to use caching (default: True)

    Returns:
        MKTestResult with trend analysis results

    Examples:
        >>> data = np.array([1, 2, 3, 4, 5])
        >>> result = mk_test_with_cache(data)
        >>> # Second call with same data uses cached result
        >>> result2 = mk_test_with_cache(data)
    """
    if not use_cache:
        return mk_test(x, alpha, seasonal, period, calculate_slope)

    # Convert to tuple for hashing
    data_tuple = _array_to_tuple(x)
    return _mk_test_cached(data_tuple, alpha, seasonal, period, calculate_slope)


def clear_cache():
    """
    Clear the Mann-Kendall test cache.

    Useful when you want to force recalculation or free up memory.

    Examples:
        >>> clear_cache()  # Clear all cached results
    """
    _mk_test_cached.cache_clear()
    logger.info("Mann-Kendall cache cleared")


def get_cache_info():
    """
    Get information about the cache performance.

    Returns:
        CacheInfo namedtuple with hits, misses, maxsize, and currsize

    Examples:
        >>> info = get_cache_info()
        >>> print(f"Cache hits: {info.hits}, misses: {info.misses}")
    """
    return _mk_test_cached.cache_info()
