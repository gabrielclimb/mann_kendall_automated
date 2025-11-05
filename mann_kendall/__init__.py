"""
Mann Kendall Automated (MKA) - A package for automated trend analysis using the Mann-Kendall test.

This package provides tools to analyze time series data for environmental engineering and geology,
automating the Mann-Kendall statistical test to identify trends in datasets.
"""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # Python < 3.8 fallback
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version("mann-kendall-automated")
except PackageNotFoundError:
    # Package not installed, use fallback version
    __version__ = "0.1.0-dev"

__author__ = "Gabriel Barbosa Soares"

# Expose main API functions
from mann_kendall.core.mann_kendall import MKTestResult, mk_test
from mann_kendall.core.processor import generate_mann_kendall
from mann_kendall.data.loader import load_excel_data

__all__ = [
    "mk_test",
    "MKTestResult",
    "generate_mann_kendall",
    "load_excel_data",
    "__version__",
    "__author__",
]