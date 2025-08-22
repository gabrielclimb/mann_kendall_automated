"""
This module implements Sen's Slope Estimator, a non-parametric method
to estimate the magnitude of trends in time series data.
"""

import numpy as np


def sens_slope(x: np.ndarray) -> float:
    """
    Calculate Sen's Slope - the median of all pairwise slopes in the time series.
    
    This is a nonparametric estimator of the slope of a trend, commonly used
    with the Mann-Kendall test to estimate the magnitude of the trend.
    
    Args:
        x (np.ndarray): A vector of time series data.
        
    Returns:
        float: The estimated slope (median of all pairwise slopes).
    """
    # Input validation
    if x is None or len(x) < 2:
        raise ValueError("Input array must contain at least 2 data points for slope calculation")
    
    n = len(x)
    
    # Generate all pairwise differences and their corresponding time differences
    # Creating indices for all possible pairs
    i, j = np.meshgrid(range(n), range(n))
    
    # Only consider pairs where j > i (upper triangle, excluding diagonal)
    mask = j > i
    
    # Calculate slopes of all pairs: (y_j - y_i) / (j - i)
    # This uses vectorized operations for better performance
    slopes = (x[j[mask]] - x[i[mask]]) / (j[mask] - i[mask])
    
    # Return the median slope
    return np.median(slopes)
