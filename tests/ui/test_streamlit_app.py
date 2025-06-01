import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from mann_kendall.ui.streamlit_app import main

def test_main_with_valid_file():
    # Mock the file uploader to return a valid file
    with patch('streamlit.file_uploader') as mock_uploader:
        mock_uploader.return_value = MagicMock(getvalue=lambda: b'valid_excel_data')
        with patch('mann_kendall.data.loader.load_excel_data') as mock_loader:
            mock_loader.return_value = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            with patch('mann_kendall.core.processor.generate_mann_kendall') as mock_generate:
                mock_generate.return_value = (pd.DataFrame({'C': [7, 8, 9]}), pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}))
                with patch('streamlit.spinner'):
                    with patch('streamlit.markdown'):
                        with patch('streamlit.sidebar'):
                            with patch('streamlit.tabs'):
                                main()

def test_main_with_empty_file():
    # Mock the file uploader to return an empty file
    with patch('streamlit.file_uploader') as mock_uploader:
        mock_uploader.return_value = MagicMock(getvalue=lambda: b'')
        with patch('streamlit.error') as mock_error:
            main()
            mock_error.assert_called_with("❌ The uploaded file is empty. Please upload a file with data.")

def test_main_with_invalid_file():
    # Mock the file uploader to return an invalid file
    with patch('streamlit.file_uploader') as mock_uploader:
        mock_uploader.return_value = MagicMock(getvalue=lambda: b'invalid_excel_data')
        with patch('mann_kendall.data.loader.load_excel_data', side_effect=pd.errors.ParserError):
            with patch('streamlit.error') as mock_error:
                main()
                mock_error.assert_called_with("❌ Unable to parse the uploaded file. Please ensure it's a valid Excel file.") 