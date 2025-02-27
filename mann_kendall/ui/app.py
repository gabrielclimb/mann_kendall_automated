#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gabriel Barbosa Soares"

import pandas as pd
import streamlit as st

from mann_kendall.core.processor import generate_mann_kendall
from mann_kendall.data.cleaner import get_columns_with_incorrect_values
from mann_kendall.data.loader import load_excel_data
from mann_kendall.ui.download import get_table_download_link
from mann_kendall.ui.visualizer import create_trend_plot, display_results_table


def main() -> None:
    """
    Main function for the Streamlit app.
    Sets up the UI and handles user interactions.
    """
    # Configure the page
    st.set_page_config(
        page_title="Mann Kendall Automated",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Header and description
    st.title("Mann Kendall Automated")
    st.markdown("""
    A tool for automated trend analysis using the Mann-Kendall test.
    Upload your Excel file to get started.
    """)

    # File uploader in sidebar
    with st.sidebar:
        st.header("Input Data")
        file_upload = st.file_uploader(
            label="Upload Excel File", type=["xlsx", "xls"]
        )
        
        # Show input format example
        with st.expander("Input Format Example"):
            st.markdown("""
            | | Point Name 1 | Point name 2 |
            | ----------------- | :----------: | -----------: |
            | date (yyyy-mm-dd) | 2004-10-01 | 2004-11-03 |
            | component | 37.1 | 12.2 |
            """)

    # Process data when file is uploaded
    if file_upload:
        try:
            # Display an informative message while processing
            with st.spinner("Processing data..."):
                # Load and process the data
                df = load_excel_data(file_upload.getvalue())
                results, dataframe = generate_mann_kendall(df)
                
                # Check for incorrect values
                if get_columns_with_incorrect_values(dataframe):
                    st.warning("⚠️ The input file contains some incorrect values. Please check and fix them for accurate results.")
                
                # Add download link to sidebar
                with st.sidebar:
                    st.markdown("### Download Results")
                    st.markdown(get_table_download_link(results), unsafe_allow_html=True)
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["Visualization", "Results Table"])
                
                with tab1:
                    create_trend_plot(results, dataframe)
                
                with tab2:
                    display_results_table(results)
                
        except pd.errors.EmptyDataError:
            st.error("❌ The uploaded file is empty. Please upload a file with data.")
        except pd.errors.ParserError:
            st.error("❌ Unable to parse the uploaded file. Please ensure it's a valid Excel file.")
        except ValueError as ve:
            st.error(f"❌ Value Error: {str(ve)}")
        except TypeError as te:
            st.error(f"❌ Type Error: {str(te)}. Please check your data types.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}. Please try again or contact support.")
    else:
        # Show instructions when no file is uploaded
        st.info("👈 Please upload an Excel file using the sidebar to begin analysis.")
        st.markdown("""
        ### About Mann-Kendall test
        
        The Mann-Kendall test is a non-parametric statistical test used to identify trends in time series data. 
        It's commonly used in environmental and geological applications to detect if there's a consistent 
        upward or downward trend in the data over time.
        
        This tool automates the process and provides clear visualizations of the results.
        """)


if __name__ == "__main__":
    main()