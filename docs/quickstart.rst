Quick Start Guide
=================

This guide will help you get started with Mann Kendall Automated in just a few minutes.

Web Interface
-------------

The easiest way to use MKA is through the web interface:

1. **Launch the app:**

   .. code-block:: bash

      streamlit run app.py

2. **Upload your Excel file** using the drag-and-drop interface

3. **View results** and download the analysis

Or try the `live demo <https://mannkendall.streamlit.app/>`_.

Command Line Interface
----------------------

For automation and batch processing:

Basic Example
~~~~~~~~~~~~~

.. code-block:: bash

   # Analyze a file
   mann-kendall data.xlsx

   # Specify output file and format
   mann-kendall data.xlsx -o results.csv --format csv

   # Verbose output with summary
   mann-kendall data.xlsx --verbose --summary

Python API
----------

Use MKA in your Python scripts:

Simple Example
~~~~~~~~~~~~~~

.. code-block:: python

   import mann_kendall as mka
   import numpy as np

   # Create sample data
   data = np.array([1.2, 1.4, 1.3, 1.7, 1.9, 2.1, 2.3])

   # Run Mann-Kendall test
   result = mka.mk_test(data)

   # Display results
   print(f"Trend: {result.trend}")
   print(f"Statistic: {result.statistic}")
   print(f"Confidence Factor: {result.confidence_factor:.2%}")
   print(f"Sen's Slope: {result.slope}")

Processing Excel Files
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import mann_kendall as mka

   # Load data
   df = mka.load_excel_data("monitoring_data.xlsx")

   # Process all wells and components
   results, transposed_data = mka.generate_mann_kendall(df)

   # Save results
   results.to_excel("analysis_results.xlsx", index=False)

   # Display summary
   print(f"Analyzed {len(results)} components")
   print(f"from {len(results['Well'].unique())} wells")

Data Format
-----------

Your Excel file should have:

* **First row:** Well names (column headers)
* **First column:** Dates (any standard format)
* **Subsequent rows:** Component names and measurements

Example:

.. code-block:: text

                    | Well-01 | Well-02 | Well-03 |
   -----------------+---------+---------+---------+
   2020-01-15       | 2020... | 2020... | 2020... |
   pH               | 7.2     | 7.5     | 6.9     |
   Temperature (°C) | 18.5    | 19.2    | 17.8    |
   Arsenic (mg/L)   | 0.015   | <0.01   | ND      |

Next Steps
----------

* Read the full :doc:`usage` guide
* Explore :doc:`examples`
* Check the :doc:`api/index` reference
* Report issues on `GitHub <https://github.com/gabrielclimb/mann_kendall_automated/issues>`_
