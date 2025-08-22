from enum import Enum
from typing import NamedTuple, Tuple, Optional

import numpy as np
from scipy.stats import norm

from mann_kendall.core.sens_slope import sens_slope


class TrendType(str, Enum):
    """Enum representing different types of trends detected by Mann-Kendall test."""
    INCREASING = "Increasing"
    DECREASING = "Decreasing"
    PROB_INCREASING = "Prob. Increasing"
    PROB_DECREASING = "Prob. Decreasing"
    NO_TREND = "No Trend"
    STABLE = "Stable"
    SEASONAL_INCREASING = "Seasonal Increasing"
    SEASONAL_DECREASING = "Seasonal Decreasing"
    SEASONAL_PROB_INCREASING = "Seasonal Prob. Increasing"
    SEASONAL_PROB_DECREASING = "Seasonal Prob. Decreasing"
    SEASONAL_NO_TREND = "Seasonal No Trend"
    SEASONAL_STABLE = "Seasonal Stable"


class MKTestResult(NamedTuple):
    """Results from a Mann-Kendall trend test."""
    trend: str  # Now returns clean string values instead of enum
    statistic: float
    coefficient_of_variation: float
    confidence_factor: float
    slope: float = 0.0


def _seasonal_mk_test(x: np.ndarray, alpha: float = 0.05, period: int = 12) -> MKTestResult:
    """
    Performs the seasonal Mann-Kendall test for trend detection in seasonal time series data.
    
    This implementation follows Hirsch, R.M., Slack, J.R., Smith, R.A. (1982).
    "Techniques of trend analysis for monthly water quality data."
    
    Args:
        x (np.ndarray): Time series data arranged sequentially
        alpha (float): Significance level
        period (int): Number of seasons (e.g., 12 for monthly data)
        
    Returns:
        MKTestResult: Results of the seasonal Mann-Kendall test
    """
    n_seasons = period
    season_length = len(x) // n_seasons
    
    # Not enough complete seasons
    if season_length < 2:
        # Fall back to regular Mann-Kendall if we don't have enough data
        return mk_test(x, alpha, seasonal=False)
    
    total_s = 0
    total_var_s = 0
    
    # Calculate S for each season
    for i in range(n_seasons):
        # Extract data for this season (e.g., all Januaries, all Februaries, etc.)
        season_data = x[i::n_seasons]
        
        # Skip seasons with too few data points
        if len(season_data) < 2:
            continue
            
        # Calculate S statistic for this season
        n = len(season_data)
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                s += np.sign(season_data[j] - season_data[k])
                
        total_s += s
        
        # Calculate variance for this season (simplified - ignoring ties for brevity)
        total_var_s += (n * (n - 1) * (2 * n + 5)) / 18
    
    # Calculate the Z statistic
    if total_s > 0:
        z = (total_s - 1) / np.sqrt(total_var_s)
    elif total_s < 0:
        z = (total_s + 1) / np.sqrt(total_var_s)
    else:
        z = 0
        
    # Calculate p-value
    p = 1 - norm.cdf(abs(z))
    
    # Coefficient of variation remains the same as non-seasonal
    cv = np.std(x, ddof=1) / np.mean(x) if abs(np.mean(x)) > 1e-10 else np.inf
    
    # Confidence factor
    cf = 1 - p
    
    # Determine trend with seasonal prefixes - return clean string values
    if cf < 0.9:
        trend = "seasonal no trend"  # Consolidate seasonal stable and no trend
    else:
        if cf <= 0.95:
            if total_s > 0:
                trend = "seasonal probably increasing"
            else:
                trend = "seasonal probably decreasing"
        else:
            if total_s > 0:
                trend = "seasonal increasing"
            else:
                trend = "seasonal decreasing"
    
    return MKTestResult(
        trend=trend,
        statistic=round(total_s, 4),
        coefficient_of_variation=round(cv, 2),
        confidence_factor=round(cf, 3)
    )


def mk_test(x: np.ndarray, alpha: float = 0.05, seasonal: bool = False, period: int = 12, 
          calculate_slope: bool = True) -> MKTestResult:
    """
    Perform the Mann-Kendall test for trend analysis in time series data.
    
    Validates input data before performing analysis.
    
    This function is derived from code originally posted by Sat Kumar Tomer
    (satkumartomer@gmail.com)
    See also: http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
    
    The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
    1987) is to statistically assess if there is a monotonic upward or downward
    trend of the variable of interest over time. A monotonic upward (downward)
    trend means that the variable consistently increases (decreases) through
    time, but the trend may or may not be linear. The MK test can be used in
    place of a parametric linear regression analysis, which can be used to test
    if the slope of the estimated linear regression line is different from
    zero. The regression analysis requires that the residuals from the fitted
    regression line be normally distributed; an assumption not required by the
    MK test, that is, the MK test is a non-parametric (distribution-free) test.
    Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
    viewed as an exploratory analysis and is most appropriately used to
    identify stations where changes are significant or of large magnitude and
    to quantify these findings.
    
    Args:
        x (np.ndarray): A vector of time series data
        alpha (float, optional): Significance level. Defaults to 0.05.
        seasonal (bool, optional): Whether to perform seasonal Mann-Kendall test. Defaults to False.
        period (int, optional): Number of seasons (e.g., 12 for monthly data). Defaults to 12.
        calculate_slope (bool, optional): Whether to calculate Sen's slope. Defaults to True.
    
    Returns:
        MKTestResult: A named tuple containing:
            - trend: Classification of trend ("Increasing", "Decreasing", "Prob. Increasing", 
              "Prob. Decreasing", "No Trend", "Stable")
            - statistic: Mann-Kendall statistic value (S)
            - coefficient_of_variation: Coefficient of variation (CV)
            - confidence_factor: Confidence factor (CF)
    
    Examples:
        >>> x = np.random.rand(100)
        >>> result = mk_test(x, 0.05)
        >>> print(f"Trend: {result.trend}, Statistic: {result.statistic}")
    """
    # Validate input data
    if x is None or len(x) < 2:
        raise ValueError("Input array must contain at least 2 data points")
    
    # Handle cases with very few data points
    if len(x) < 4:
        # For fewer than 4 points, we can still calculate but results are less reliable
        # Return a simple trend based on first and last values
        if len(x) == 2:
            trend = "increasing" if x[1] > x[0] else "decreasing" if x[1] < x[0] else "no trend"
            return MKTestResult(
                trend=trend,
                statistic=1.0 if x[1] > x[0] else -1.0 if x[1] < x[0] else 0.0,
                coefficient_of_variation=np.std(x, ddof=1) / np.mean(x) if np.mean(x) != 0 else 0.0,
                confidence_factor=0.5  # Low confidence due to insufficient data
            )
        elif len(x) == 3:
            # Simple comparison for 3 points
            s = np.sign(x[1] - x[0]) + np.sign(x[2] - x[0]) + np.sign(x[2] - x[1])
            trend = "increasing" if s > 0 else "decreasing" if s < 0 else "no trend"
            return MKTestResult(
                trend=trend,
                statistic=float(s),
                coefficient_of_variation=np.std(x, ddof=1) / np.mean(x) if np.mean(x) != 0 else 0.0,
                confidence_factor=0.6  # Low confidence due to insufficient data
            )
    
    # Check if input contains NaN values
    if np.isnan(x).any():
        raise ValueError("Input array contains NaN values")
    
    # Check if all values are identical
    if np.all(x == x[0]):
        return MKTestResult(
            trend="no trend", 
            statistic=0.0,
            coefficient_of_variation=0.0,
            confidence_factor=0.0
        )
    
    n = len(x)
    
    if seasonal:
        # Make sure we have enough data for seasonal analysis
        if n < period * 2:
            raise ValueError(f"Seasonal Mann-Kendall requires at least {period * 2} data points")
            
        # Perform seasonal Mann-Kendall test
        return _seasonal_mk_test(x, alpha, period)
    
    # Calculate S more efficiently using vectorized operations
    # This is faster for large arrays compared to the nested loop approach
    # Create a matrix of differences
    i, j = np.meshgrid(np.arange(n), np.arange(n))
    signs = np.sign(x[j] - x[i])
    
    # We only need upper triangle (excluding diagonal)
    mask = i < j
    s = np.sum(signs[mask])

    # calculate the unique data
    unique_x = np.unique(x)
    g = len(unique_x)

    # Calculate the variance of S
    if n == g:  # No ties in the data
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else:  # Handle ties more efficiently using np.unique with return_counts
        # Get counts of each unique value
        _, counts = np.unique(x, return_counts=True)
        
        # Only consider ties (values that appear more than once)
        tie_counts = counts[counts > 1]
        
        # Calculate variance with tie correction
        tie_correction = np.sum(tie_counts * (tie_counts - 1) * (2 * tie_counts + 5))
        var_s = (n * (n - 1) * (2 * n + 5) - tie_correction) / 18

    # Calculate standardized test statistic Z
    # The formula includes a continuity correction (+/- 1)
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)  # Continuity correction for positive S
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)  # Continuity correction for negative S
    elif s == 0:
        z = 0

    # Calculate additional statistics used for trend classification
    
    # Coefficient of Variation - measures relative variability
    # Using ddof=1 for sample standard deviation
    # Handle the case where mean is very close to zero to avoid division errors
    mean_value = np.mean(x)
    if abs(mean_value) < 1e-10:  # Threshold for "practically zero"
        cv = np.inf if np.std(x, ddof=1) > 0 else 0.0
    else:
        cv = np.std(x, ddof=1) / mean_value
    
    # Calculate the p-value (one-tailed test)
    p = 1 - norm.cdf(abs(z))
    
    # We don't use this result directly, but keep the calculation for reference
    _ = abs(z) > norm.ppf(1 - alpha)
    
    # Confidence Factor - derived from p-value
    cf = 1 - p

    # Determine trend classification based on confidence factor, s value, and coefficient of variation
    # Always return clean string values, not enum objects
    if cf < 0.9:  # Low confidence (< 90%)
        trend = "no trend"  # Consolidate stable and no trend into single category
    else:  # Higher confidence (>= 90%)
        if cf <= 0.95:  # Between 90% and 95% confidence
            if s > 0:
                trend = "probably increasing"  # Probable increasing trend
            else:
                trend = "probably decreasing"  # Probable decreasing trend
        else:  # Above 95% confidence
            if s > 0:
                trend = "increasing"  # Strong increasing trend
            else:
                trend = "decreasing"  # Strong decreasing trend

    # Calculate Sen's slope if requested
    slope = 0.0
    if calculate_slope:
        try:
            slope = sens_slope(x)
        except Exception:
            # If slope calculation fails, we'll still return results with slope=0
            pass

    # Return a named tuple for better readability and type hinting
    return MKTestResult(
        trend=trend,
        statistic=round(s, 4),
        coefficient_of_variation=round(cv, 2),
        confidence_factor=round(cf, 3),
        slope=round(slope, 6)
    )