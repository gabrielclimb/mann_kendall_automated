# Description: Main Streamlit app for the Mann Kendall Automated tool.
# ruff: noqa: E501
__author__ = "Gabriel Barbosa Soares"

import pandas as pd
import streamlit as st
from typing import Optional, Tuple

from mann_kendall.core.processor import generate_mann_kendall
from mann_kendall.data.cleaner import get_columns_with_incorrect_values
from mann_kendall.data.loader import load_excel_data, check_data_sufficiency
from mann_kendall.ui.download import get_table_download_link, create_enhanced_download_section
from mann_kendall.ui.visualizer import create_trend_plot, display_results_table


def validate_file_format(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate if the uploaded file has the correct format.

    Args:
        df: The loaded DataFrame

    Returns:
        Tuple of (is_valid, error_message)
    """
    if df.empty:
        return False, "The file is empty. Please upload a file with data."

    if df.shape[0] < 2:
        return False, "The file must have at least 2 rows (dates and at least one component)."

    if df.shape[1] < 2:
        return (
            False,
            "The file must have at least 2 columns (one for dates and at least one data column).",
        )

    # Skip strict date validation - let users proceed and handle format issues during processing
    # The actual data processing will handle various date formats more robustly

    return True, ""


def display_data_preview(df: pd.DataFrame) -> None:
    """Display a preview of the uploaded data with basic statistics."""
    st.subheader("📊 Data Preview")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("**First 10 rows of your data:**")
        st.dataframe(df.head(10), use_container_width=True)

    with col2:
        st.write("**Data Summary:**")
        st.metric("Total Rows", df.shape[0])
        st.metric("Total Columns", df.shape[1])
        st.metric("Data Points", f"{(df.shape[0] - 1) * (df.shape[1] - 1):,}")

        # Check for missing values
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            st.warning(f"⚠️ {missing_count} missing values detected")
        else:
            st.success("✅ No missing values")


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
        initial_sidebar_state="expanded",
    )

    # Header and description
    st.title("📈 Mann Kendall Automated")
    st.markdown("""
    **Automated trend analysis using the Mann-Kendall statistical test**
    
    Perfect for environmental engineering and geology applications. Upload your Excel file to detect trends in your time series data.
    """)

    # File uploader in sidebar
    with st.sidebar:
        st.header("📁 Input Data")

        # Add file size limit info
        st.caption("Maximum file size: 200MB")

        file_upload = st.file_uploader(
            label="Upload Excel File",
            type=["xlsx", "xls"],
            help="Upload your Excel file with time series data",
        )

        # Show input format example with better formatting
        with st.expander("📋 Required Format", expanded=False):
            st.markdown("""
            **Your Excel file should be structured like this:**
            
            | | Well_1 | Well_1 | Well_1 |
            |---|--------|--------|--------|
            | | **2020-01-01** | **2020-02-01** | **2020-03-01** |
            | **Nitrate** | 15.2 | 16.1 | 17.3 |
            | **Chloride** | 45.2 | 44.8 | 43.9 |
            | **pH** | 7.2 | 7.1 | 7.3 |
            
            **Important:**
            - **Row 1**: Well names (can repeat for multiple time periods)
            - **Row 2**: Dates for each measurement (yyyy-mm-dd format)
            - **Row 3+**: Component name in first column + values for each well/date combination
            - Use "ND" or "N/D" for non-detected values
            """)

        # Add helpful tips
        with st.expander("💡 Tips for Best Results"):
            st.markdown("""
            - Ensure at least 5 data points per well for reliable results
            - Use consistent date formats
            - Remove any header rows except column names
            - Check for typos in well names and dates
            """)

    # Initialize session state for data persistence
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = None
        st.session_state.results = None

    # Process data when file is uploaded
    if file_upload:
        try:
            # Step 1: Load and validate data
            with st.spinner("📂 Loading your file..."):
                df = load_excel_data(file_upload.getvalue())

            # Step 2: Validate file format
            is_valid, error_msg = validate_file_format(df)
            if not is_valid:
                st.error(f"❌ **File Format Error:** {error_msg}")
                st.info("💡 Please check the format requirements in the sidebar and try again.")
                return

            # Step 3: Show data preview
            display_data_preview(df)

            # Step 3.5: Check data sufficiency and show warnings
            is_sufficient, warning_msg = check_data_sufficiency(df)
            if not is_sufficient:
                st.warning(f"⚠️ **Data Sufficiency Warning:** {warning_msg}")
                st.info(
                    "💡 You can still proceed with the analysis, but results may be less reliable."
                )
            elif warning_msg:
                st.info(f"ℹ️ **Data Quality Note:** {warning_msg}")

            # Step 4: Processing confirmation
            if st.button("🚀 Run Mann-Kendall Analysis", type="primary", use_container_width=True):
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # Step 5: Process the data with progress updates
                    status_text.text("🔄 Transposing and cleaning data...")
                    progress_bar.progress(25)

                    results, dataframe = generate_mann_kendall(df)
                    progress_bar.progress(75)

                    status_text.text("✅ Analysis complete!")
                    progress_bar.progress(100)

                    # Store results in session state
                    st.session_state.results = results
                    st.session_state.processed_data = dataframe

                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()

                    # Success message with summary
                    st.success(f"""
                    🎉 **Analysis Complete!**
                    - Processed **{len(results.Well.unique())} wells**
                    - Analyzed **{len(results)} well-component combinations**
                    - Found **{len(results[results.Trend != "no trend"])} significant trends**
                    """)

                    # Check for data quality issues
                    if get_columns_with_incorrect_values(dataframe):
                        st.warning("""
                        ⚠️ **Data Quality Notice:** Some values in your data couldn't be converted to numbers. 
                        These have been handled automatically, but you may want to review your source data for accuracy.
                        """)

                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    raise e

        except pd.errors.EmptyDataError:
            st.error(
                "❌ **Empty File:** The uploaded file contains no data. Please check your file and try again."
            )
        except pd.errors.ParserError:
            st.error(
                "❌ **File Parse Error:** Unable to read the Excel file. Please ensure it's a valid .xlsx or .xls file."
            )
        except ValueError as ve:
            st.error(f"❌ **Data Error:** {str(ve)}")
            st.info(
                "💡 This usually means there's an issue with your data format. Please check the format requirements."
            )
        except TypeError as te:
            st.error(f"❌ **Type Error:** {str(te)}")
            st.info("💡 This typically occurs when data contains text where numbers are expected.")
        except MemoryError:
            st.error(
                "❌ **Memory Error:** The file is too large to process. Please try with a smaller dataset."
            )
        except Exception as e:
            st.error(f"❌ **Unexpected Error:** {str(e)}")
            st.info("💡 If this persists, please check your data format or contact support.")

    # Display results if they exist in session state
    if st.session_state.results is not None and st.session_state.processed_data is not None:
        st.divider()

        # Add enhanced download section to sidebar
        with st.sidebar:
            create_enhanced_download_section(
                st.session_state.results, st.session_state.processed_data
            )

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📈 Visualization", "📋 Results Table", "📊 Summary"])

        with tab1:
            create_trend_plot(st.session_state.results, st.session_state.processed_data)

        with tab2:
            display_results_table(st.session_state.results)

        with tab3:
            display_summary_statistics(st.session_state.results)

    elif not file_upload:
        # Show welcome screen when no file is uploaded
        st.markdown("---")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            ### 🎯 What is Mann-Kendall Analysis?
            
            The Mann-Kendall test is a **non-parametric statistical test** used to detect trends in time series data. 
            It's particularly valuable because it:
            
            - ✅ Doesn't assume normal distribution
            - ✅ Handles missing data well
            - ✅ Robust against outliers
            - ✅ Widely accepted in environmental science
            """)

        with col2:
            st.markdown("""
            ### 🔬 Perfect for:
            
            - **Environmental Monitoring** - Groundwater quality trends
            - **Geology** - Subsidence or uplift detection  
            - **Climate Studies** - Temperature and precipitation trends
            - **Water Resources** - Flow and level monitoring
            - **Contamination Assessment** - Pollutant concentration changes
            """)

        st.info(
            "👆 **Ready to get started?** Upload your Excel file using the sidebar to begin your trend analysis!"
        )


def display_summary_statistics(results: pd.DataFrame) -> None:
    """Display summary statistics and insights from the analysis."""
    st.subheader("📊 Analysis Summary")

    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Wells", len(results.Well.unique()))
    with col2:
        st.metric("Components", len(results.Analise.unique()))
    with col3:
        st.metric("Total Tests", len(results))
    with col4:
        significant_trends = len(results[results.Trend != "no trend"])
        st.metric("Significant Trends", significant_trends)

    # Component analysis
    if len(results.Analise.unique()) > 1:
        st.subheader("🧪 Component Analysis")
        component_trends = results.groupby(["Analise", "Trend"]).size().unstack(fill_value=0)
        st.dataframe(component_trends, use_container_width=True)


if __name__ == "__main__":
    main()
