Mann Kendall Automated Documentation
====================================

Welcome to the documentation for **Mann Kendall Automated (MKA)**, a comprehensive
Python tool for performing the Mann-Kendall statistical test on time series data.

MKA is designed specifically for environmental engineering and geology applications,
automating trend detection in datasets such as groundwater monitoring, contaminant
concentrations, and water quality assessments.

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   usage
   api/index
   examples
   contributing
   changelog

Quick Links
-----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Overview
--------

Features
~~~~~~~~

* 🖥️ **Web Interface**: Beautiful Streamlit web application
* ⌨️ **CLI Tool**: Command-line interface for batch processing
* 📊 **Export Results**: Download results as Excel, CSV, or JSON
* 📈 **Interactive Visualizations**: Dynamic trend plots with Plotly
* ✅ **Data Validation**: Automatic detection of invalid data
* 🔬 **Statistical Rigor**: Proper Mann-Kendall implementation
* 🎯 **Sen's Slope**: Trend magnitude estimation included

Installation
~~~~~~~~~~~~

Install using pip:

.. code-block:: bash

   pip install mann-kendall-automated

Or from source:

.. code-block:: bash

   git clone https://github.com/gabrielclimb/mann_kendall_automated.git
   cd mann_kendall_automated
   pip install -e .

Quick Example
~~~~~~~~~~~~~

.. code-block:: python

   import mann_kendall as mka
   import numpy as np

   # Perform Mann-Kendall test
   data = np.array([1.2, 1.4, 1.3, 1.7, 1.9, 2.1, 2.3])
   result = mka.mk_test(data)

   print(f"Trend: {result.trend}")
   print(f"Confidence: {result.confidence_factor:.2%}")
   print(f"Sen's Slope: {result.slope}")

Support
-------

* 📖 `Documentation <https://mann-kendall-automated.readthedocs.io/>`_
* 🐛 `Issue Tracker <https://github.com/gabrielclimb/mann_kendall_automated/issues>`_
* 💬 `Discussions <https://github.com/gabrielclimb/mann_kendall_automated/discussions>`_

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
