# Development Guide

This guide provides instructions for setting up a local development environment for the Mann Kendall Automated (MKA) project using rye, a modern Python packaging and project management tool.

## Prerequisites

1. Python: Ensure Python is installed on your system. Verify the installation with:
   ```bash
   python --version
   ```

2. Git: Make sure Git is installed. Verify with:
   ```bash
   git --version
   ```

3. Rye: Install rye by following the instructions in the [rye documentation](https://rye-up.com/guide/installation/).

## Setting Up the Development Environment

1. Clone the MKA repository:
   ```bash
   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   ```

2. Set up the project environment and install dependencies:
   ```bash
   rye sync
   ```
   This command creates a virtual environment, installs all project dependencies, and creates a lock file if it doesn't exist.

## Development Workflow

Rye provides several commands to manage your project:

1. Add a new dependency:
   ```bash
   rye add <package-name>
   ```

2. Add a development dependency:
   ```bash
   rye add --dev <package-name>
   ```

3. Update dependencies:
   ```bash
   rye sync
   ```

4. Run the Streamlit app:
   ```bash
   rye run stream
   ```

5. Run tests:
   ```bash
   rye run test
   ```

6. Update requirements.txt:
   ```bash
   rye run req
   ```

## Pre-commit Setup

1. Install pre-commit:
   ```bash
   rye add --dev pre-commit
   ```

2. Set up the git hook scripts:
   ```bash
   pre-commit install
   ```

## Linting

Run linting checks with:
```bash
rye run lint
```
This executes all pre-commit hooks against all files.

## Testing

Run the test suite with:
```bash
rye run test
```
This runs pytest, clears the cache before running tests, and measures code coverage of the source code in the src directory.

## Project Structure

- `src/`: Contains the main source code
- `tests/`: Contains test files
- `pyproject.toml`: Defines project metadata and dependencies
- `.pre-commit-config.yaml`: Configures pre-commit hooks

## Best Practices

1. Always use `rye run` to execute scripts defined in `pyproject.toml`.
2. Keep `pyproject.toml` up to date with all project dependencies.
3. Run linting and tests before committing changes.
4. Use pre-commit hooks to maintain code quality.

## Conclusion

You now have a local development environment set up for the MKA project using rye. Start contributing by creating new features or fixing bugs. Ensure you follow the project's coding standards and use pre-commit checks to maintain code quality.

For any questions or issues, please refer to the project's issue tracker on GitHub.
