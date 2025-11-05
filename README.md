
<div align="center">
  <img src="docs/images/logo.png" alt="Mann Kendall Automated Logo" width="300" height="300">

  # Mann Kendall Automated (MKA)

  **Automated Trend Analysis for Environmental Engineering and Geology**

  [![Tests](https://github.com/gabrielclimb/mann_kendall_automated/workflows/Python%20Tests/badge.svg)](https://github.com/gabrielclimb/mann_kendall_automated/actions)
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

  [🌐 Live Demo](https://mannkendall.streamlit.app/) | [📖 Documentation](#documentation) | [🐛 Report Bug](https://github.com/gabrielclimb/mann_kendall_automated/issues) | [✨ Request Feature](https://github.com/gabrielclimb/mann_kendall_automated/issues)

</div>

---

## 📋 Overview

Mann Kendall Automated (MKA) is a comprehensive Python tool for performing the **Mann-Kendall statistical test** on time series data. Designed specifically for environmental engineering and geology applications, it automates trend detection in datasets such as:

- 🏭 Groundwater monitoring data
- 🧪 Contaminant concentration trends
- 🌡️ Temperature and pH measurements
- 💧 Well water quality assessments
- 📊 Any time-series environmental data

### Why MKA?

✅ **Save Time**: Automate what used to take hours in spreadsheets
✅ **Reliable**: Implements standard Mann-Kendall methodology with Sen's slope
✅ **Flexible**: Web interface, CLI, or Python API
✅ **Visual**: Interactive plots with Plotly
✅ **Robust**: Handles missing data, detection limits, and data validation

## ✨ Features

- 🖥️ **Web Interface**: Beautiful Streamlit web application with drag-and-drop file upload
- ⌨️ **CLI Tool**: Command-line interface for batch processing and automation
- 📊 **Export Results**: Download results as Excel, CSV, or JSON
- 📈 **Interactive Visualizations**: Dynamic trend plots with Plotly
- ✅ **Data Validation**: Automatic detection and reporting of invalid data
- 🔬 **Statistical Rigor**: Proper Mann-Kendall implementation with seasonal variant support
- 🎯 **Sen's Slope**: Trend magnitude estimation included
- 🔄 **Batch Processing**: Analyze multiple wells and components simultaneously
- ⚡ **Performance**: Optimized with caching for repeated analyses

## 💖 Support This Project

<a href="https://www.buymeacoffee.com/gabrielsoares"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=gabrielsoares&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

If this project helps you, please consider supporting it!
## 🚀 Quick Start

### Installation

#### Using pip (Recommended)

```bash
pip install mann-kendall-automated
```

#### From Source

```bash
git clone https://github.com/gabrielclimb/mann_kendall_automated.git
cd mann_kendall_automated
pip install -e .
```

#### For Development

```bash
git clone https://github.com/gabrielclimb/mann_kendall_automated.git
cd mann_kendall_automated
pip install -e ".[dev]"
pre-commit install  # Set up git hooks
```

## 📖 Usage

### 1. Web Application

Launch the interactive web interface:

```bash
streamlit run app.py
```

Or try the **[live demo](https://mannkendall.streamlit.app/)** hosted on Streamlit Cloud!

**Features:**
- Drag-and-drop file upload
- Real-time data validation
- Interactive trend plots
- Download results as Excel/CSV

### 2. Command Line Interface (CLI)

Perfect for automation and batch processing:

#### Basic Usage

```bash
# Analyze a file (outputs to <filename>_mann_kendall_results.xlsx)
mann-kendall data.xlsx

# Specify output file
mann-kendall data.xlsx -o results.xlsx

# Export as CSV
mann-kendall data.xlsx --format csv

# Verbose mode with summary
mann-kendall data.xlsx --verbose --summary
```

#### Advanced Options

```bash
# Enable debug logging
mann-kendall data.xlsx --log-level DEBUG

# Save logs to file
mann-kendall data.xlsx --log-file analysis.log

# JSON export for further processing
mann-kendall data.xlsx --format json -o results.json
```

### 3. Python API

Use MKA programmatically in your scripts:

```python
import mann_kendall as mka
import numpy as np

# Simple trend test
data = np.array([1.2, 1.4, 1.3, 1.7, 1.9, 2.1, 2.3])
result = mka.mk_test(data)

print(f"Trend: {result.trend}")
print(f"Statistic: {result.statistic}")
print(f"Confidence: {result.confidence_factor:.2%}")
print(f"Sen's Slope: {result.slope}")

# Load and process Excel file
df = mka.load_excel_data("monitoring_data.xlsx")
results, transposed_data = mka.generate_mann_kendall(df)

# Export results
results.to_excel("analysis_results.xlsx", index=False)
```

## 📊 Input Data Format

Your Excel file should follow this structure:

|                   | Well-01 | Well-02 | Well-03 |
| ----------------- | :-----: | :-----: | :-----: |
| 2020-01-15        | 2020-01-15 | 2020-01-20 | 2020-01-18 |
| pH                | 7.2     | 7.5     | 6.9     |
| Temperature (°C)  | 18.5    | 19.2    | 17.8    |
| Arsenic (mg/L)    | 0.015   | <0.01   | ND      |
| Lead (mg/L)       | 0.003   | 0.002   | 0.004   |

**Format Requirements:**
- **First row**: Well names (column headers)
- **First column**: Dates in any standard format (YYYY-MM-DD, MM/DD/YYYY, etc.)
- **Subsequent rows**: Component names and measurements
- **Special values**:
  - `ND`, `N/D`, `NOT DETECTED` → Treated as 0.5 (configurable)
  - `<0.01` → Detection limit used (0.01)
  - Empty cells → Ignored in analysis

**📁 Example Files:**
Check the `examples/` directory for sample datasets you can use to test MKA.

## 📈 Output

MKA generates a comprehensive results table with:

| Column | Description |
|--------|-------------|
| **Well** | Well identifier |
| **Analise** | Component/parameter name |
| **Trend** | Trend classification (Increasing, Decreasing, No Trend, etc.) |
| **Mann-Kendall Statistic (S)** | Test statistic value |
| **Coefficient of Variation** | Relative variability measure |
| **Confidence Factor** | Statistical confidence (0-1) |

**Trend Classifications:**
- `increasing` - Strong increasing trend (>95% confidence)
- `decreasing` - Strong decreasing trend (>95% confidence)
- `probably increasing` - Moderate increasing trend (90-95% confidence)
- `probably decreasing` - Moderate decreasing trend (90-95% confidence)
- `no trend` - No statistically significant trend (<90% confidence)

## Project Structure

The project follows a modular architecture:

```
mann_kendall_automated/
├── app.py                  # Main entry point for Streamlit app
├── mann_kendall/           # Main package
│   ├── core/               # Core functionality
│   │   ├── mann_kendall.py # Statistical implementation
│   │   └── processor.py    # Data processing logic
│   ├── data/               # Data handling
│   │   ├── loader.py       # File loading functionality
│   │   └── cleaner.py      # Data cleaning
│   ├── ui/                 # UI components
│   │   ├── app.py          # Streamlit app
│   │   ├── visualizer.py   # Plotting functionality
│   │   └── download.py     # Export functionality
│   └── utils/              # Utilities
│       └── progress.py     # Progress bar
├── scripts/                # CLI scripts
│   └── mann_kendall_cli.py # Command line interface
├── tests/                  # Unit and integration tests
└── examples/               # Example data and notebooks
```

## Development

For developers:

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dev dependencies: `pip install -e ".[dev]"`
4. Run tests: `pytest`

## License

MIT

## Credits

- Core Mann-Kendall implementation adapted from code by Sat Kumar Tomer
- Original implementation based on the GSI Spreadsheet

Visit the [MKA GitHub repository](https://github.com/gabrielclimb/mann_kendall_automated) to learn more.
