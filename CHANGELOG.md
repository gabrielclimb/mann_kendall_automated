# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modular package structure for better code organization
- Command-line interface for batch processing
- Improved documentation with migration guide
- Example scripts for API and CLI usage
- Test structure with pytest fixtures
- GitHub Actions workflow for CI/CD

### Changed
- Reorganized code into mann_kendall package
- Separated concerns: core, data, UI, and utilities
- Enhanced Streamlit UI with tabs and improved layout
- Updated dependency management with pyproject.toml
- Migrated to uv for Python package management

### Fixed
- Better error handling in data loading
- Clearer warning messages for invalid data
- Fixed test failures in Mann-Kendall trend detection
- Fixed string handling for values with '<' prefix
- Fixed issue with detecting invalid values in columns

## [0.2.0] - 2024-09-26

### Added
- Added error handling for file uploads in Streamlit app
- Added validation for incorrect data values 

### Changed
- Refactored to use context manager with pd.ExcelWriter for better resource management
- Updated development documentation to use uv package manager
- Added type hints to function signatures

### Fixed
- Fixed string_test function to properly handle values with '<' prefix
- Fixed get_columns_with_incorrect_values function for better data validation

## [0.1.0] - 2024-03-20

### Changed
- Removed deprecated features in Streamlit app
- Updated development environment setup

### Security
- Bumped Pillow from 9.5.0 to 10.2.0
- Bumped Streamlit from 1.23.1 to 1.30.0
- Bumped PyArrow from 12.0.0 to 14.0.1
- Bumped SciPy from 1.9.1 to 1.10.0
- Bumped Protobuf from 3.20.1 to 3.20.2

## [0.0.1] - 2023-06-08

### Added
- Initial release with basic functionality
- Added logo image to README
- Streamlit web application
- Mann-Kendall trend detection implementation
- Excel file input and output support