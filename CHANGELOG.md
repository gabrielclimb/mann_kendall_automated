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

### Fixed
- Better error handling in data loading
- Clearer warning messages for invalid data

## [0.0.1] - 2023-01-01

### Added
- Initial release with basic functionality
- Streamlit web application
- Mann-Kendall trend detection implementation
- Excel file input and output support