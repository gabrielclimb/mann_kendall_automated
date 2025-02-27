from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def filter_well_component(
    df_transposed: pd.DataFrame, desired_wells: list, desired_component: str
) -> pd.DataFrame:
    """
    Filters the DataFrame to include only the desired wells and component.

    Args:
        df_transposed (pd.DataFrame): Transposed DataFrame.
        desired_wells (list): List of desired wells.
        desired_component (str): Desired component selected by the user.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    df_filtered = df_transposed[df_transposed.well.isin(desired_wells)]
    df_filtered = df_filtered[["well", "Date", desired_component]].sort_values("Date")
    df_filtered[desired_component] = df_filtered[desired_component].apply(float)
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def get_desired_component(results: pd.DataFrame, desired_wells: List[str]) -> str:
    """
    Gets the desired component selected by the user.

    Args:
        results (pd.DataFrame): Results of the Mann Kendall test.
        desired_wells (list): List of desired wells.

    Returns:
        str: Desired component selected by the user.
    """
    results_filter_by_well = results[results.Well.isin(desired_wells)]
    desired_component = st.selectbox(
        "Select Component", results_filter_by_well.Analise.unique()
    )
    return desired_component


def choose_log_scale() -> bool:
    """
    Allows the user to choose between a logarithmic or linear scale for the y-axis.

    Returns:
        bool: True if log scale is selected, False otherwise.
    """
    log_scale = st.selectbox("Select Scale", ["Log", "Linear"])
    return log_scale == "Log"


def create_trend_plot(results: pd.DataFrame, dataframe: pd.DataFrame) -> None:
    """
    Creates and displays an interactive plot of selected wells and components.

    Args:
        results (pd.DataFrame): Results of the Mann Kendall test.
        dataframe (pd.DataFrame): DataFrame containing the data.
    """
    desired_wells = st.multiselect("Select Well", results.Well.unique())

    if len(desired_wells):
        desired_component = get_desired_component(results, desired_wells)
        df_filtered = filter_well_component(dataframe, desired_wells, desired_component)
        df_filtered = df_filtered.dropna()
        log_scale = choose_log_scale()

        # Prepare data for plotting
        df_plot = df_filtered.reset_index(drop=True).ffill()
        
        # Handle log scale properly
        if log_scale:
            # Check for zeros or negative values
            min_value = df_plot[desired_component].min()
            
            # Create a new column for log-transformed values
            log_component_name = f"{desired_component}_log"
            
            if min_value <= 0:
                st.warning(
                    f"Data contains zeros or negative values which can't be displayed on log scale."
                    f"Minimum value found: {min_value}. "
                    f"Non-positive values will be replaced with a small positive number."
                )
                # Replace zeros or negative values with a small positive number
                # (1% of the smallest positive value or 0.001 if no positive values exist)
                positive_min = df_plot[df_plot[desired_component] > 0][desired_component].min()
                replacement_value = positive_min * 0.01 if not pd.isna(positive_min) else 0.001
                
                # Create a copy of the column with replacements for log transformation
                df_plot[log_component_name] = df_plot[desired_component].copy()
                (
                    df_plot.loc[
                        df_plot[log_component_name] <= 0, log_component_name
                        ]
                ) = replacement_value
                
                # Now apply log transformation
                df_plot[log_component_name] = np.log10(df_plot[log_component_name])
                
                # Add a note about replacement to the chart title
                title =(
                    f"""{', '.join(desired_wells)} x {desired_component} 
                    d(log scale with replaced values)""")
                plot_component = log_component_name
            else:
                # No replacement needed, just log transform
                df_plot[log_component_name] = np.log10(df_plot[desired_component])
                title = f"{', '.join(desired_wells)} x {desired_component} (log scale)"
                plot_component = log_component_name
                
            # Set log_y to False since we're manually doing the log transform
            log_y_setting = False
        else:
            # For linear scale, use the original component
            title = f"{', '.join(desired_wells)} x {desired_component} (linear scale)"
            plot_component = desired_component
            log_y_setting = False

        fig = px.line(
            df_plot,
            x="Date",
            y=plot_component,
            color="well",
            log_y=log_y_setting,
            title=title,
        )
        
        # Customize Y-axis label to show the original component name
        fig.update_layout(yaxis_title=desired_component)

        st.plotly_chart(fig, use_container_width=True)


def display_results_table(results: pd.DataFrame) -> None:
    """
    Displays the results table with filtering options.
    
    Args:
        results (pd.DataFrame): Results of the Mann Kendall test.
    """
    st.subheader("Mann-Kendall Test Results")
    
    # Add filtering options
    well_filter = st.multiselect("Filter by Wells", options=results.Well.unique(), default=[])
    trend_filter = st.multiselect("Filter by Trend", options=results.Trend.unique(), default=[])
    
    # Apply filters if selected
    filtered_results = results
    if well_filter:
        filtered_results = filtered_results[filtered_results.Well.isin(well_filter)]
    if trend_filter:
        filtered_results = filtered_results[filtered_results.Trend.isin(trend_filter)]
    
    # Display the filtered results
    st.dataframe(filtered_results, use_container_width=True)