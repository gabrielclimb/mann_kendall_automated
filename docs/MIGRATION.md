# Migration Guide

This guide helps users migrate from the previous structure to the new modular architecture of Mann Kendall Automated.

## Changes Overview

The Mann Kendall Automated project has been restructured to follow modern Python package development standards. The main changes include:

1. **Modular Package Structure**: The core functionality is now organized into a proper Python package
2. **Separation of Concerns**: UI, data handling, and core functionality are separated
3. **Command Line Interface**: A new CLI has been added for batch processing
4. **Better Configuration**: More flexible configuration options
5. **Improved Documentation**: Better docs and examples

## For Users

### Web Application Users

If you've been using the web application, you can continue to do so with no changes:

- The online version at [Streamlit Cloud](https://mannkendall.streamlit.app/) works the same
- To run locally, use `streamlit run app.py` as before

### For Script Users

If you were previously importing functions directly from the old structure:

1. **Old import**:
```python
from src.generate import generate_mann_kendall
```

2. **New import**:
```python
from mann_kendall.core.processor import generate_mann_kendall
```

### New CLI Tool

A new command-line interface is now available:

```bash
mann-kendall input_file.xlsx -o results.xlsx
```

## For Developers

### Package Installation

Install the package in development mode:

```bash
pip install -e ".[dev]"
```

### Running Tests

Run tests using pytest:

```bash
pytest
```

### Using the New Structure

The new structure separates concerns:
- `mann_kendall/core/`: Core statistical functionality
- `mann_kendall/data/`: Data loading and cleaning
- `mann_kendall/ui/`: User interface components
- `mann_kendall/utils/`: Utility functions

### Extending the Package

To add new features:
1. Add core functionality to the appropriate module
2. Write tests for your additions
3. Update UI components as needed
4. Update documentation

## Additional Resources

- See the updated [README.md](/README.md) for an overview of the new structure
- Check the [examples](/examples) directory for usage examples
- Review the [Development Guide](/DEVELOPMENT.md) for development guidelines