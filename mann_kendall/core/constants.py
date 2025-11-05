"""
Constants used throughout the Mann-Kendall analysis package.

This module centralizes all magic numbers and configuration values used in the
statistical analysis and data processing.
"""

# Statistical Test Thresholds
CONFIDENCE_THRESHOLD_LOW = 0.9  # 90% confidence threshold
CONFIDENCE_THRESHOLD_HIGH = 0.95  # 95% confidence threshold
DEFAULT_ALPHA = 0.05  # Default significance level for statistical tests
ZERO_THRESHOLD = 1e-10  # Threshold for considering values as "practically zero"

# Data Quality Requirements
MIN_SAMPLES_FOR_ANALYSIS = 5  # Minimum samples required for well to be analyzed
MIN_SAMPLES_PER_COMPONENT = 4  # Minimum samples per component for Mann-Kendall test
MIN_POINTS_FOR_RELIABLE_TEST = 6  # Recommended minimum for reliable statistical test
MIN_POINTS_FOR_SEASONAL = 2  # Minimum complete seasons for seasonal analysis

# Data Cleaning and Conversion
NOT_DETECTED_VALUE = 0.5  # Default value to use for "ND" (not detected) markers
NOT_DETECTED_MARKERS = ("ND", "N/D", "NOT DETECTED", "nd", "n/d")  # Recognized ND markers

# Seasonal Analysis
DEFAULT_PERIOD = 12  # Default number of seasons (monthly data)

# File Processing
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB maximum file size for uploads
SUPPORTED_FILE_EXTENSIONS = ('.xlsx', '.xls')  # Supported Excel file formats

# Output Formatting
DECIMAL_PLACES_STATISTIC = 4  # Decimal places for Mann-Kendall statistic
DECIMAL_PLACES_CV = 2  # Decimal places for coefficient of variation
DECIMAL_PLACES_CF = 3  # Decimal places for confidence factor
DECIMAL_PLACES_SLOPE = 6  # Decimal places for Sen's slope

# Trend Classifications
TREND_INCREASING = "increasing"
TREND_DECREASING = "decreasing"
TREND_PROB_INCREASING = "probably increasing"
TREND_PROB_DECREASING = "probably decreasing"
TREND_NO_TREND = "no trend"
TREND_STABLE = "stable"

# Seasonal Trend Classifications
SEASONAL_TREND_INCREASING = "seasonal increasing"
SEASONAL_TREND_DECREASING = "seasonal decreasing"
SEASONAL_TREND_PROB_INCREASING = "seasonal probably increasing"
SEASONAL_TREND_PROB_DECREASING = "seasonal probably decreasing"
SEASONAL_TREND_NO_TREND = "seasonal no trend"
SEASONAL_TREND_STABLE = "seasonal stable"

# Low Confidence Values (for insufficient data)
LOW_CONFIDENCE_2_POINTS = 0.5
LOW_CONFIDENCE_3_POINTS = 0.6
