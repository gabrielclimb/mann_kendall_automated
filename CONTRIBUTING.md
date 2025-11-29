# Contributing to Mann Kendall Automated (MKA)

Thank you for your interest in contributing to Mann Kendall Automated! This document provides guidelines for contributing to the project.

## Quick Start

For a quick development setup, see the Development section in [README.md](README.md).

For detailed development instructions, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Project Information

- **Version**: 0.2.0 (as specified in pyproject.toml)
- **Python Requirements**: 3.8 or higher
- **License**: MIT
- **Repository**: https://github.com/gabrielclimb/mann_kendall_automated

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher (as specified in pyproject.toml)
- Git
- [uv](https://github.com/astral-sh/uv) (recommended) or other Python environment manager

### Setup Instructions

Please refer to [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for comprehensive setup instructions.

## Code Quality Standards

We use the following tools to maintain code quality:

- **Ruff**: For linting and code formatting (primary tool)
- **Black**: For code formatting (legacy, being phased out)  
- **isort**: For import sorting
- **pytest**: For testing

Note: The project is transitioning to use Ruff for both linting and formatting to simplify the toolchain.

## Testing

Run tests with:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=mann_kendall
```

## Documentation

This project maintains several documentation files:

- [README.md](README.md) - Main project documentation and user guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - This file, contribution guidelines
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Detailed development guide
- [docs/MIGRATION.md](docs/MIGRATION.md) - Migration guide
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes

### Documentation Cross-References

The documentation files are interconnected:
- README.md → CONTRIBUTING.md (for contribution guidelines)
- README.md → docs/DEVELOPMENT.md (for detailed development setup)
- CONTRIBUTING.md → docs/DEVELOPMENT.md (for comprehensive instructions)
- docs/DEVELOPMENT.md → README.md (for quick start)
- docs/DEVELOPMENT.md → CONTRIBUTING.md (for contribution workflow)

Please ensure all documentation remains consistent in terminology and version information.

### Documentation Consistency Guidelines

When updating documentation, ensure:

1. **Version Information**: All version references match pyproject.toml (currently 0.2.0)
2. **Project Name**: Use "Mann Kendall Automated" or "MKA" consistently
3. **Python Requirements**: Always reference "Python 3.8 or higher" as specified in pyproject.toml
4. **Cross-References**: Update links between documentation files when adding new content
5. **Tool References**: Mention the transition to Ruff for both linting and formatting

## Related Resources

- [Project Homepage](https://github.com/gabrielclimb/mann_kendall_automated)
- [Issue Tracker](https://github.com/gabrielclimb/mann_kendall_automated/issues)
- [Streamlit App](https://mannkendall.streamlit.app/)

---

*This document is part of the Mann Kendall Automated project documentation suite. For the most up-to-date information, please refer to the project repository.*