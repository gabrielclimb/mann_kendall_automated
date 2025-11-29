# Mann Kendall Automated (MKA) - GitHub Copilot Instructions

Mann Kendall Automated is a Python statistical analysis tool for environmental engineering and geology that performs automated Mann-Kendall trend analysis on time series data. The project includes a Streamlit web application, command-line interface, and core statistical analysis library.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Environment Setup

**CRITICAL - Network Dependencies**: Dependency installation often fails due to firewall limitations. Set timeouts of 60+ minutes and be prepared for failures.

#### Preferred Setup (uv)
```bash
# Install uv (may fail due to network restrictions)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up environment - NEVER CANCEL: Takes 3-5 minutes. Set timeout to 10+ minutes
uv sync
```

#### Alternative Setup (pip) 
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode - NEVER CANCEL: Takes 3-5 minutes. Set timeout to 10+ minutes  
pip install -e .

# Install development dependencies - NEVER CANCEL: Takes 2-3 minutes. Set timeout to 8+ minutes
pip install pytest pytest-cov black isort ruff
```

**NOTE**: If pip install fails with "Read timed out", "Could not resolve host", or "TimeoutError", this indicates firewall/network limitations. This is EXPECTED in restricted environments - document the failure and proceed with syntax validation only.

### Build and Test

```bash
# Syntax validation (always works) - Takes ~15 seconds
find . -name "*.py" -exec python -m py_compile {} \;

# Run tests (requires dependencies) - NEVER CANCEL: Takes 30-60 seconds. Set timeout to 5+ minutes
pytest tests/ --cov=mann_kendall

# Alternative test command for CI compatibility
pytest --cache-clear --cov=src src/tests/

# Linting (requires tools) - Takes 10-30 seconds each
black mann_kendall tests scripts
isort mann_kendall tests scripts  
ruff check mann_kendall tests scripts
```

### Run Applications

#### Web Application
```bash
# ALWAYS activate environment first
source venv/bin/activate  # or . .venv/bin/activate for uv

# Start Streamlit web app - NEVER CANCEL: App startup takes 30-60 seconds
streamlit run app.py
```

#### Command Line Interface
```bash
# Show help
mann-kendall --help

# Process Excel file
mann-kendall input_file.xlsx -o results.xlsx --verbose

# Using Python directly if CLI not installed
python scripts/mann_kendall_cli.py input_file.xlsx -o results.xlsx
```

## Validation

**ALWAYS manually validate any changes by running through complete scenarios.**

### Required Validation Scenarios
1. **Syntax Check**: Run `find . -name "*.py" -exec python -m py_compile {} \;` - Must complete without errors in ~14 seconds
2. **Individual Module**: Test `python -m py_compile mann_kendall/core/processor.py` - Should succeed even without dependencies
3. **CLI Help** (if dependencies available): Execute `python scripts/mann_kendall_cli.py --help`
4. **Import Test**: Try `python -c "from mann_kendall.core import processor"` - Will fail with "No module named 'pandas'" if dependencies missing
5. **Web App** (if dependencies available): Start `streamlit run app.py` and verify it loads the Mann-Kendall interface
6. **Example Processing** (if dependencies available): Run `python examples/basic_usage.py` with sample data to test end-to-end workflow
7. **Test Suite** (if dependencies available): Execute `pytest tests/` and verify core statistical functions work correctly

### Manual Testing Workflow
After making changes, ALWAYS:
1. Test CLI with sample Excel file from `examples/example_input_table.xlsx`
2. Verify web app loads and can process sample data
3. Check that results are saved correctly to Excel format
4. Validate Mann-Kendall statistical output matches expected format

### Pre-commit Validation
```bash
# Format code
black mann_kendall tests scripts
isort mann_kendall tests scripts

# Check for issues - NEVER CANCEL: Takes 30 seconds. Set timeout to 2+ minutes  
ruff check mann_kendall tests scripts

# Run full test suite before committing
pytest tests/ --cov=mann_kendall
```

## Common Tasks

### Project Structure
```
mann_kendall_automated/
├── app.py                  # Streamlit web application entry point
├── mann_kendall/           # Core analysis library
│   ├── core/              # Mann-Kendall statistical functions
│   ├── data/              # Data loading and cleaning  
│   ├── ui/                # Streamlit UI components
│   └── utils/             # Utility functions
├── scripts/               # Command-line tools
│   └── mann_kendall_cli.py # CLI interface
├── tests/                 # Modern test suite (use this)
├── src/tests/             # Legacy test suite (deprecated)
├── examples/              # Usage examples and sample data
└── docs/                  # Documentation
```

### Quick References

#### Repository Stats
- **Languages**: Python 3.8+  
- **Files**: 440 Python files, ~122k lines of code
- **Dependencies**: Streamlit, pandas, scipy, openpyxl, plotly
- **Test Framework**: pytest with coverage
- **Linting**: black, isort, ruff, pylint

#### Time Expectations
- **Syntax Check**: ~14 seconds for 440 Python files - NEVER CANCEL
- **Dependency Install**: 3-5 minutes (often fails due to network) - NEVER CANCEL: Set timeout to 10+ minutes
- **Test Suite**: 30-60 seconds (requires dependencies) - NEVER CANCEL: Set timeout to 5+ minutes  
- **Linting**: 10-30 seconds per tool (requires dependencies) - NEVER CANCEL: Set timeout to 2+ minutes
- **App Startup**: 30-60 seconds (requires streamlit) - NEVER CANCEL

#### Common File Patterns
- **Main entry points**: `app.py`, `scripts/mann_kendall_cli.py`
- **Core logic**: `mann_kendall/core/processor.py`, `mann_kendall/core/mann_kendall.py`
- **Tests**: `tests/` (preferred), `src/tests/` (legacy)
- **Examples**: `examples/basic_usage.py`, `examples/example_input_table.xlsx`
- **Config**: `pyproject.toml`, `requirements.txt`, `.pre-commit-config.yaml`

### Troubleshooting

### Troubleshooting

#### Network/Dependency Issues
- **Symptom**: `pip install` fails with "Read timed out", "HTTPSConnectionPool timeout", or "Could not resolve host"
- **Solution**: Document as "fails due to firewall/network limitations" - this is expected in restricted environments
- **Workaround**: Use syntax checking and code analysis without full dependency installation

#### Module Import Errors  
- **Symptom**: `ModuleNotFoundError: No module named 'pandas'` when running app.py or CLI
- **Solution**: Ensure virtual environment is activated and dependencies installed with `pip install -e .`
- **Alternative**: Add project root to PYTHONPATH: `export PYTHONPATH=$PWD:$PYTHONPATH` (limited functionality)

#### CLI/App Startup Failures
- **Symptom**: Scripts fail with import errors for pandas, streamlit, matplotlib
- **Expected**: This occurs when dependencies aren't installed due to network restrictions
- **Solution**: Only attempt functional testing after successful dependency installation

#### Test Failures
- **Symptom**: Tests fail due to missing sample data or import errors
- **Solution**: Ensure you're in project root and `examples/example_input_table.xlsx` exists
- **Note**: Some tests require actual Excel files and statistical libraries - do not run with mock data

## CI/CD Integration

The project uses GitHub Actions with:
- **Matrix Testing**: Python 3.8, 3.9, 3.10 on Ubuntu
- **Required Checks**: ruff linting, pytest with coverage
- **Build Process**: uv sync, dependency caching
- **Timeout Settings**: Default 5-minute job timeout

When making changes, ensure they pass:
```bash
# Local CI validation
ruff check mann_kendall tests scripts
pytest --cov=mann_kendall tests/
```