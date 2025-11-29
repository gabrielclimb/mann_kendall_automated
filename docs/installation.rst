Installation
============

Requirements
------------

Mann Kendall Automated requires Python 3.8 or higher.

Using pip (Recommended)
-----------------------

The easiest way to install Mann Kendall Automated is using pip:

.. code-block:: bash

   pip install mann-kendall-automated

This will install the latest stable release from PyPI along with all required dependencies.

From Source
-----------

To install from source (for development or to get the latest unreleased features):

.. code-block:: bash

   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   pip install -e .

Development Installation
------------------------

If you want to contribute to the project, install with development dependencies.

**Option 1: Using pip (recommended)**

.. code-block:: bash

   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   pip install -e ".[dev]"
   pre-commit install

**Option 2: Using uv (Recommended)**

.. code-block:: bash

   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   uv sync

Both methods install additional tools for:

* Testing (pytest, pytest-cov)
* Code formatting (black, isort, ruff)
* Type checking (mypy)
* Pre-commit hooks

Verifying Installation
----------------------

To verify that Mann Kendall Automated is installed correctly:

.. code-block:: python

   import mann_kendall as mka
   print(mka.__version__)

Or check the CLI tool:

.. code-block:: bash

   mann-kendall --help

Dependencies
------------

Required packages (automatically installed):

* pandas >= 2.2.2
* numpy >= 2.1.0
* scipy >= 1.14.1
* streamlit >= 1.38.0
* plotly >= 5.24.0
* openpyxl >= 3.1.5
* xlrd >= 2.0.1
* xlsxwriter >= 3.2.0

Optional dependencies for development:

* pytest, pytest-cov (testing)
* black, isort, ruff (code formatting)
* mypy (type checking)

Optional dependencies for documentation:

* sphinx, sphinx-rtd-theme (documentation generation)
* sphinx-autodoc-typehints (type hint support in docs)
* myst-parser (Markdown support in Sphinx)

Building Documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   # Install documentation dependencies
   pip install -e ".[docs]"

   # Build HTML documentation
   cd docs
   sphinx-build -b html . _build/html

   # View the documentation
   # Open docs/_build/html/index.html in your browser
