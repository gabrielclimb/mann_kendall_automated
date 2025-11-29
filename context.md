# Mann Kendall Automated (MKA) - Agent Context

## Project Overview
Mann Kendall Automated (MKA) is a Python tool for performing Mann-Kendall statistical tests on time series data, specifically designed for environmental engineering and geology (e.g., groundwater monitoring).

## Tech Stack
- **Language**: Python 3.8+
- **Web Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Testing**: Pytest
- **Formatting**: Black

## Project Structure
- `mann_kendall/`: Core package source code
    - `core/`: Statistical implementation and processors
    - `data/`: Data loading and cleaning
    - `ui/`: Streamlit application components
- `app.py`: Main entry point for the Streamlit web app
- `scripts/`: CLI tools
- `tests/`: Unit and integration tests

## Development Guidelines
- **Code Style**: Follow `black` formatting.
- **Testing**: Run tests using `pytest`. Ensure new features have test coverage.
- **Documentation**: Keep docstrings updated.
- **Dependency Management**: Uses `pip` or `uv` (recommended).

## Key Features
1. **Web Interface**: Streamlit app for drag-and-drop analysis.
2. **CLI**: Command-line tool for batch processing.
3. **Python API**: Library usage for scripts.
4. **Outputs**: Excel, CSV, JSON, and interactive plots.

## Repository Analysis & Future Improvements
### Observations
- **Dependency Management**: The project uses `uv` for dependency management (configured in `pyproject.toml`).
- **Testing**:
    - Tests are located in `tests/` and use `pytest`.
    - `tests/conftest.py` provides shared fixtures (sample DataFrames, arrays).
    - `tests/core/test_mann_kendall.py` validates trend detection logic.
- **Cleanup**: `test_trend_fix.py` in the root directory appears to be a temporary verification script that can be removed.
- **CI/CD**: GitHub Actions are configured in `.github/workflows` for tests and app deployment.

### Suggested Improvements
1. **Remove Temporary Files**: Delete `test_trend_fix.py` to keep the root directory clean.
2. **Standardize Dev Setup**: `uv` is the primary recommendation for dependency management.
3. **Test Coverage**: Ensure `mann_kendall/core/processor.py` and UI components have adequate test coverage.

