import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))

from mann_kendall_automated.utils.fix_string import string_test,\
    string_to_float, get_columns_with_incorrect_values
from mann_kendall_automated.utils.mann_kendall import mk_test
from mann_kendall_automated.generate import generate_mann_kendall,\
    transpose_dataframe
