# Mann Kendall Automated

The idea of this project is automated the Mann Kendall Statistc for Well, commonly use in environment engineering and geology.
The core part of code was made by [Sat Kumar Tomer](http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm) and also adapt from [GSI SpreadSheet ](https://www.gsi-net.com/en/software/free-software/gsi-mann-kendall-toolkit.html).

The code is in **`generate_kendall_stats.py`**, a example input table is **`input_tables/tabela_exemplo_input.xlsx`** and **`utils/kendall_dist.csv`** is a table with value for normal curve that was extract from GSI cause it was a little different from those values usually used with numpy

To run the script you should be inside of `mann_kendall_automated` folder.

To run directly in command line:
```bash
python3 generate_kendall_stats.py
```
