<div style="text-align: center;">
  <img src="docs/images/logo.png" alt="Logo" style="width: 300px; height: 300px;">
</div>

# Mann Kendall Automated (MKA)

A Time-Saving Solution for Environmental Engineering and Geology

## Overview

Mann Kendall Automated (MKA) is a tool for performing the Mann-Kendall statistical test on time series data, particularly focused on environmental engineering and geology applications. It automates trend detection in datasets such as well monitoring data.

## Features

- **Web Interface**: Easy-to-use Streamlit web application
- **CLI Tool**: Command-line interface for batch processing
- **Export Results**: Download results as Excel files
- **Interactive Visualizations**: Plot trends with Plotly
- **Data Validation**: Automatically detect and report invalid data

## Installation

### Using pip

```bash
pip install mann-kendall-automated
```

### From source

```bash
git clone https://github.com/gabrielclimb/mann_kendall_automated.git
cd mann_kendall_automated
pip install -e .
```

## Usage

### Web Application

Run the web app locally:

```bash
streamlit run app.py
```

Or visit the hosted version at [Streamlit Cloud](https://mannkendall.streamlit.app/).

### Command Line Interface

Process files directly from the command line:

```bash
mann-kendall input_file.xlsx -o results.xlsx
```

## Input Format

Your data should be formatted as follows:

|                   | Point Name 1 | Point name 2 |
| ----------------- | :----------: | -----------: |
| date (yyyy-mm-dd) |  2004-10-01  |   2004-11-03 |
| component         |     37.1     |         12.2 |

See examples in the `examples/` directory.

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