[![Build Status](https://travis-ci.org/gabrielclimb/mann_kendall_automated.svg?branch=master)](https://travis-ci.org/gabrielclimb/mann_kendall_automated)

# Mann Kendall Automated

The idea of this project is automated the Mann Kendall Statistc for Well, commonly use in environment engineering and geology.
The core part of code was made by [Sat Kumar Tomer](http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm) and also adapt from [GSI SpreadSheet ](https://www.gsi-net.com/en/software/free-software/gsi-mann-kendall-toolkit.html).

The code is in **`generate_kendall_stats.py`**, a example input table is **`input_tables/example_input_table.xlsx`** and **`utils/kendall_dist.csv`** is a table with value for normal curve that was extract from GSI cause it was a little different from those values usually used with numpy

To run directly in command line:
```bash
python3 main.py
```

The result will be saved in **`output_tables/`** with follow format: *`filename_NowDate_RandomNumber.xlsx`*
