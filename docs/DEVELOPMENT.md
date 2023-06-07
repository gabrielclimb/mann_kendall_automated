# Development Guide

This guide provides instructions for setting up a local development environment for the Mann Kendall Automated (MKA) project.

## Prerequisites

1. Ensure Python is installed on your system. You can verify the installation by running the following command in your terminal:
    ```bash
    python --version
    ```
2. Ensure Git is installed on your system. You can verify the installation by running the following command in your terminal:
    ```bash
    git --version
    ```

## Steps to Set Up the Local Development Environment

1. Clone the MKA repository to your local machine using the command:
    ```bash
    git clone https://github.com/gabrielclimb/mann_kendall_automated.git
    ```
2. Navigate to the cloned repository directory:
    ```bash
    cd mann_kendall_automated
    ```
3. Install `virtualenv` using pip, Python's package installer:
    ```bash
    pip install virtualenv
    ```
4. Create a virtual environment in the project directory:
    ```bash
    virtualenv .venv
    ```
5. Activate the virtual environment:
    - On Unix or MacOS, run:
        ```bash
        source .venv/bin/activate
        ```
    - On Windows, run:
        ```bash
        .venv\Scripts\activate
        ```
6. Install the dependencies required for MKA:
    ```bash
    pip install -r dev-requirements.txt
    ```

## Pre-commit setup

1. Install pre-commit:
    ```bash
    pip install pre-commit
    ```
2. Set up the git hook scripts:
    ```bash
    pre-commit install
    ```

This will add the pre-commit script to your `.git/hooks/pre-commit` directory.

## Makefile Usage

The `Makefile` in the MKA repository contains a set of directives used to running linting checks and tests.

### Linting

Linting refers to the process of analyzing source code to flag programming errors, bugs, stylistic errors, and suspicious constructs. This process helps in maintaining code consistency and avoiding potential issues that might come up during runtime.

In the context of this project, the `lint` command is used to run pre-commit checks on all files. This includes checks for code formatting, import order, type hinting, and more, depending on the hooks configured in your `.pre-commit-config.yaml`.

You can run the linting checks with the command:

```bash
make lint
```
This command runs pre-commit run --all-files, which executes all pre-commit hooks against all the files.

### Testing
Testing is a crucial part of software development. It's a process where the code is executed in a controlled environment to ascertain its correctness.

In this project, the test command is used to run the test suite using pytest, a testing framework for Python that allows you to easily create small, simple tests, yet scales to support complex functional testing.

The command to run the tests is:

```bash
make test
```

This command runs pytest --cache-clear --cov=src src/tests/, which clears the cache (--cache-clear) before running the tests, and also measures code coverage (--cov=src) of the source code in the src directory. The tests themselves are located in the src/tests/ directory.

## Conclusion

Now, you have a local development environment set up for the MKA project. You can start contributing to the project by creating new features or fixing bugs. Please ensure to follow the coding standards defined in the project and make use of the pre-commit checks to maintain the code quality.
