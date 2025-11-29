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
```

### Testing
```bash
# Run all tests
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

# CLI
mann-kendall input.xlsx -o results.xlsx --verbose
```

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

**`data/`** - Data I/O
- `loader.py` - Excel file loading with validation (`load_excel_data()`)
- `cleaner.py` - Handles special values: "ND"/"N/D" → 0.5, "<0.01" → detection limit, empty → NaN

**`ui/`** - Presentation layer
- `app.py` - Streamlit UI components
- `visualizer.py` - Interactive Plotly charts
- `download.py` - Export to Excel/CSV/JSON

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

## CI

GitHub Actions runs on Python 3.8-3.12: `ruff check` then `pytest --cov=mann_kendall tests/`
