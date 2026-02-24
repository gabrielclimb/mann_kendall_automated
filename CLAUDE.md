# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mann Kendall Automated (MKA) is a Python tool for performing Mann-Kendall statistical trend analysis on time series data, designed for environmental engineering and geology applications (groundwater monitoring, contaminant trends, water quality assessments).

## Common Commands

### Development Setup
```bash
# Using uv (recommended)
uv sync

# Alternative: pip
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Testing
```bash
# Run all tests (use tests/, not legacy src/tests/)
pytest

# Run tests with coverage
pytest --cov=mann_kendall

# Run a single test file
pytest tests/test_mann_kendall.py

# Run a specific test
pytest tests/test_mann_kendall.py::test_function_name
```

### Linting and Formatting
```bash
# Lint check
ruff check mann_kendall tests scripts

# Format code
black mann_kendall tests scripts
isort mann_kendall tests scripts
```

### Running the Application
```bash
# Web interface (Streamlit)
streamlit run app.py
# Live demo: https://mannkendall.streamlit.app/

# CLI - basic usage
mann-kendall input.xlsx -o results.xlsx --verbose

# CLI - advanced options
mann-kendall input.xlsx --format csv --log-level DEBUG --summary
mann-kendall input.xlsx --format json --log-file analysis.log

# Using Python directly if CLI not installed
python scripts/mann_kendall_cli.py input.xlsx -o results.xlsx
```

### Documentation
```bash
# Build documentation (requires pip install -e ".[docs]")
pip install -e ".[docs]"
cd docs
sphinx-build -b html . _build/html
# Open docs/_build/html/index.html in browser
```

### Example Data
Sample data for testing is available in `examples/` directory, including `example_input_table.xlsx`.

## Architecture

### Entry Points
- `app.py` - Streamlit web application entry point
- `scripts/mann_kendall_cli.py` - CLI tool (`mann-kendall` command)

### Core Package (`mann_kendall/`)

**`core/`** - Statistical engine
- `mann_kendall.py` - Main `mk_test()` function implementing Mann-Kendall test with tie correction. Returns `MKTestResult` namedtuple with trend classification, S statistic, coefficient of variation, confidence factor, and slope.
- `sens_slope.py` - Sen's slope estimation (median of pairwise slopes)
- `processor.py` - Orchestrates analysis via `generate_mann_kendall()` and `transpose_dataframe()`
- `constants.py` - Statistical thresholds, data requirements, special markers (ND, N/D)
- `cache.py` - Caching for performance optimization

**`data/`** - Data I/O
- `loader.py` - Excel file loading with validation (`load_excel_data()`, `check_data_sufficiency()`)
- `cleaner.py` - Handles special values: "ND"/"N/D" → 0.5, "<0.01" → detection limit, empty → NaN

**`ui/`** - Presentation layer
- `app.py` - Streamlit UI components with session state management
- `visualizer.py` - Interactive Plotly charts (`create_trend_plot()`, `display_results_table()`)
- `download.py` - Export to Excel/CSV/JSON via `create_enhanced_download_section()`

**`utils/`** - Utilities
- `logging_config.py` - Configurable logging setup for CLI
- `progress.py` - Progress bar utilities

### Data Flow
```
Excel Input → loader.py → cleaner.py → processor.py (transpose)
→ mann_kendall.py + sens_slope.py (per well/component)
→ Results DataFrame → UI/CLI/Export
```

### Input Format
Excel with wells as columns, dates in first data row per well, components as row headers. Special values: `ND`, `N/D`, `<detection_limit`.

### Trend Classifications
- `increasing`/`decreasing`: >95% confidence
- `probably increasing`/`probably decreasing`: 90-95% confidence
- `no trend`: <90% confidence

## Code Style

- Line length: 130 characters
- Python 3.8+ target
- Tools: ruff (lint), black (format), isort (imports)
- Profiles: `isort` uses "black" profile

## Python API Usage

MKA can be used programmatically:

```python
import mann_kendall as mka
import numpy as np

# Simple trend test on array
data = np.array([1.2, 1.4, 1.3, 1.7, 1.9, 2.1, 2.3])
result = mka.mk_test(data)
print(f"Trend: {result.trend}")
print(f"Confidence: {result.confidence_factor:.2%}")
print(f"Sen's Slope: {result.slope}")

# Process Excel file
df = mka.load_excel_data("monitoring_data.xlsx")
results, transposed_data = mka.generate_mann_kendall(df)
results.to_excel("analysis_results.xlsx", index=False)
```

## CI

GitHub Actions runs on Python 3.8-3.12: `ruff check` then `pytest --cov=mann_kendall tests/`
