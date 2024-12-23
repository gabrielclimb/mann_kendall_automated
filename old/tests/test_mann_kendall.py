import numpy as np

from .context import mk_test


def test_mk_test():
    # Test with random data
    x = np.random.rand(100)
    trend, s, cv, cf = mk_test(x, 0.05)
    assert isinstance(trend, str)
    assert isinstance(s, float)
    assert isinstance(cv, float)
    assert isinstance(cf, float)

    # Test with an increasing trend
    x = np.arange(100)
    trend, s, cv, cf = mk_test(x, 0.05)
    assert trend in ["Increasing", "Prob. Increasing"]

    # Test with a decreasing trend
    x = np.arange(100, 0, -1)
    trend, s, cv, cf = mk_test(x, 0.05)
    assert trend in ["Decreasing", "Prob. Decreasing"]

    # Test with constant data
    x = np.full(100, 0.5)
    trend, s, cv, cf = mk_test(x, 0.05)
    assert trend in ["Stable", "No Trend"]

    # Test with a significance level of 0.1
    x = np.random.rand(100)
    trend, s, cv, cf = mk_test(x, 0.1)
    assert isinstance(trend, str)
    assert isinstance(s, float)
    assert isinstance(cv, float)
    assert isinstance(cf, float)
