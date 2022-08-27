[![Build Status](https://travis-ci.org/gabrielclimb/mann_kendall_automated.svg?branch=master)](https://travis-ci.org/gabrielclimb/mann_kendall_automated)

# Mann Kendall Automated (MKA)

The idea of this project is automated the Mann Kendall Statistc for Well, commonly use in environment engineering and geology.
The core part of code was made by [Sat Kumar Tomer](http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm) and also adapt from [GSI SpreadSheet ](https://www.gsi-net.com/en/software/free-software/gsi-mann-kendall-toolkit.html).

## How to use
 **MKA** is deployed at heroku ([https://mann-kendall.herokuapp.com/](https://mann-kendall.herokuapp.com/)), so you can use it for free. The input should be in the follow format:

|                   | Point Name 1 | Point name 2 |
| ----------------- | :----------: | -----------: |
| date (yyyy-mm-dd) |  2004-10-01  |   2004-11-03 |
| component         |     37.1     |         12.2 |

You can find some examples in [*input_tables* folder](input_tables).

### Running locally
If for any reason you want to run **MKA** locally you have to follow those steps:

1. Check if you have python in your pc: `python --version`
2. Clone this repo : `git clone https://github.com/gabrielclimb/mann_kendall_automated.git`
3. Set Up a local enviroment:
    ```bash
    pip install virtualenv
    virtualenv .venv # create virtual env
    source .venv/bin/activate # activate the virtualenv
    pip install -r requirements.txt # install MKA dependencies
    ```
4. Run