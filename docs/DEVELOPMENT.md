# Development Guide

This guide provides instructions for developers who want to contribute to Mann Kendall Automated.

## Setting Up the Development Environment

### Prerequisites

- Python 3.8 or later
- Git
- [Rye](https://rye-up.com/) (recommended) or other Python environment manager

### Setup with Rye (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   ```

2. Set up the environment with Rye:
   ```bash
   rye sync
   ```

3. Activate the environment:
   ```bash
   . .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Alternative Setup (without Rye)

1. Clone the repository:
   ```bash
   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   pip install pytest pytest-cov black isort ruff
   ```

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

## Development Workflow

### Code Style

We use the following tools to maintain code quality:

- **Black**: For code formatting
- **isort**: For import sorting
- **Ruff**: For linting

Run them with:

```bash
black mann_kendall tests scripts
isort mann_kendall tests scripts
ruff check mann_kendall tests scripts
```

### Running Tests

Run tests with pytest:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=mann_kendall
```

### Adding New Features

When adding new features:

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write tests for your feature first

3. Implement your feature

4. Ensure all tests pass

5. Submit a pull request

### Documentation

- Update docstrings for all public functions and classes
- Keep the README.md updated with any new features
- Add examples for new functionality

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new GitHub release with release notes
4. If using Rye:
   ```bash
   rye build
   rye publish
   ```
   
   If not using Rye:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## CI/CD

GitHub Actions are used for:
- Running tests
- Checking code style
- Building and publishing releases

## Additional Resources

- [Rye Documentation](https://rye-up.com/guide/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Mann-Kendall Test Documentation](http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm)
- [Pandas Documentation](https://pandas.pydata.org/docs/)