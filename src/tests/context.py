import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# pylint: disable=unused-import
from src.generate import generate_mann_kendall, transpose_dataframe
from src.utils.fix_string import (
    get_columns_with_incorrect_values,
    string_test,
    string_to_float,
)
from src.utils.mann_kendall import mk_test
from src.utils.progress_bar import print_progress_bar
