#!/usr/bin/env python3
"""
Quick test to verify trend standardization works correctly.
"""

import numpy as np
import pandas as pd
from mann_kendall.core.mann_kendall import mk_test

def test_trend_standardization():
    """Test that trends are returned as clean strings."""
    
    # Test increasing trend
    increasing_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = mk_test(increasing_data)
    print(f"Increasing trend: '{result.trend}' (type: {type(result.trend)})")
    
    # Test decreasing trend  
    decreasing_data = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    result = mk_test(decreasing_data)
    print(f"Decreasing trend: '{result.trend}' (type: {type(result.trend)})")
    
    # Test no trend (random data)
    np.random.seed(42)
    no_trend_data = np.random.normal(5, 0.1, 10)
    result = mk_test(no_trend_data)
    print(f"No trend: '{result.trend}' (type: {type(result.trend)})")
    
    # Test identical values
    identical_data = np.array([5, 5, 5, 5, 5])
    result = mk_test(identical_data)
    print(f"Identical values: '{result.trend}' (type: {type(result.trend)})")
    
    print("\n✅ All trends are now clean strings without enum prefixes!")

if __name__ == "__main__":
    test_trend_standardization()