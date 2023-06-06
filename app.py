#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gabriel Barbosa Soares"

import base64
from io import BytesIO
from typing import Tuple, List

import pandas as pd
import plotly.express as px
import streamlit as st

from src.generate import generate_mann_kendall

st.set_option("deprecation.showfileUploaderEncoding", False)


def main() -> None:
    """
    Function responsible for running the Streamlit app.
    """
    st.set_page_config("Mann Kendall Automated")

    st.title(body="Mann Kendall Automated")

    file_upload = st.sidebar.file_uploader(
        label="Upload Excel File", type=["xlsx", "xls"]
    )

    if file_upload:

        results, dataframe = cache_generate_mann_kendall(file_upload)

        st.sidebar.markdown(get_table_download_link(results), unsafe_allow_html=True)

        plot_online(results, dataframe)


@st.cache_data
def cache_generate_mann_kendall(file) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Caches the generate_mann_kendall function to avoid re-computation.

    Arguments:
        file {File} -- Uploaded Excel file.

    Returns:
        tuple -- Tuple containing the results and the DataFrame.
    """
    return generate_mann_kendall(file.getvalue())


def get_table_download_link(dataframe: pd.DataFrame) -> str:
    """
    Generates a button to download a file.

    Arguments:
        dataframe {pd.DataFrame} -- DataFrame to be downloaded.

    Returns:
        str -- HTML string representing a button with a href as stream.
    """
    val = to_excel(dataframe)
    b64 = base64.b64encode(val)
    # TODO: Create a random number as filename, check generate_xlsx
    return (
        '<p style="text-align:center;">'
        f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
        'download="mann_kendall.xlsx">Download Excel file</a></p>'
    )
    # decode b'abc' => abc)


def to_excel(dataframe: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to Excel format and returns it as bytes.

    Arguments:
        dataframe {pd.DataFrame} -- DataFrame to be converted to Excel format.

    Returns:
        bytes -- Excel file as bytes.
    """

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    dataframe.to_excel(writer, index=False, sheet_name="Sheet1")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def plot_online(results, dataframe: pd.DataFrame) -> None:
    """
    Plots the data online using Plotly.

    Arguments:
        results -- Results of the Mann Kendall test.
        dataframe {pd.DataFrame} -- DataFrame containing the data.
    """
    desired_wells = st.multiselect("Select Well", results.Well.unique())

    if len(desired_wells):

        desired_component = get_desired_component(results, desired_wells)

        df_filtered = filter_well_component(dataframe, desired_wells, desired_component)
        df_filtered = df_filtered.dropna()
        # df_filtered = fillna(df_filtered, desired_component)
        log_scale = choose_log_scale()

        name = ", ".join(desired_wells)

        fig = px.line(
            df_filtered.reset_index(drop=True).fillna(method="pad"),
            x="Date",
            y=desired_component,
            color="well",
            log_y=log_scale,
            title=f"{name} x {desired_component}",
            # width=300,
            # height=600
        )

        st.plotly_chart(fig, use_container_width=True)


def get_desired_component(results: pd.DataFrame, desired_wells: List[str]) -> str:
    """
    Gets the desired component selected by the user.

    Arguments:
        results {pd.DataFrame} -- Results of the Mann Kendall test.
        desired_wells {list} -- List of desired wells.

    Returns:
        str -- Desired component selected by the user.
    """
    results_filter_by_well = results[results.Well.isin(desired_wells)]
    desired_component = st.selectbox(
        "Select Component", results_filter_by_well.Analise.unique()
    )
    return desired_component


def filter_well_component(
    df_transposed: pd.DataFrame, desired_well: list, desired_component: str
) -> pd.DataFrame:
    """
    Filters the DataFrame to include only the desired wells and component.

    Arguments:
        df_transposed {pd.DataFrame} -- Transposed DataFrame.
        desired_well {list} -- List of desired wells.
        desired_component {str} -- Desired component selected by the user.

    Returns:
        pd.DataFrame -- Filtered DataFrame.
    """

    df_filtered = df_transposed[df_transposed.well.isin(desired_well)]

    df_filtered = df_filtered[["well", "Date", desired_component]].sort_values("Date")
    df_filtered[desired_component] = df_filtered[desired_component].apply(float)
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def choose_log_scale() -> bool:
    """
    Allows the user to choose between a logarithmic or linear scale for the y-axis.

    Returns:
        bool -- True if log scale is selected, False otherwise.
    """
    log_scale = st.selectbox("Select Scale", ["Log", "Linear"])
    if log_scale == "Log":
        return True
    return False


def fillna(df_filtered: pd.DataFrame, component: str) -> pd.DataFrame:
    """
    Fills missing values in the DataFrame.

    Arguments:
        df_filtered {pd.DataFrame} -- Filtered DataFrame.
        component {str} -- Component selected by the user.

    Returns:
        pd.DataFrame -- DataFrame with missing values filled.
    """
    df_concat = pd.DataFrame()
    for well in df_filtered.well.unique():
        df_temp = df_filtered.query(f"well=='{well}'").sort_values("Date")
        df_temp[component] = df_temp[component].fillna(method="ffill", limit=1)
        df_concat = pd.concat([df_temp, df_concat])
    return df_concat


if __name__ == "__main__":
    main()
