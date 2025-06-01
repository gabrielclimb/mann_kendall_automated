import pytest
import pandas as pd
from mann_kendall.ui.download import to_excel, get_table_download_link, generate_output_filename, save_to_excel
import os

def test_to_excel():
    # Create a sample DataFrame
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    excel_bytes = to_excel(df)
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0

def test_get_table_download_link():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    link = get_table_download_link(df, filename="test")
    assert "data:application/octet-stream;base64," in link
    assert "test.xlsx" in link

def test_generate_output_filename():
    filename = generate_output_filename("test.xlsx")
    assert "test_" in filename
    assert ".xlsx" not in filename

def test_save_to_excel():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    output_path = save_to_excel(df, "test")
    assert os.path.exists(output_path)
    os.remove(output_path)  # Clean up 