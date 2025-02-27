from typing import List

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

        name = ", ".join(desired_wells)

        fig = px.line(
            df_filtered.reset_index(drop=True).fillna(method="pad"),
            x="Date",
            y=desired_component,
            color="well",
            log_y=log_scale,
            title=f"{name} x {desired_component}",
        )

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