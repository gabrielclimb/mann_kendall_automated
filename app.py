#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gabriel Barbosa Soares"

import base64
from io import BytesIO

import streamlit as st
import pandas as pd
import plotly.express as px

from mann_kendall_automated.generate import generate_mann_kendall

st.set_option('deprecation.showfileUploaderEncoding', False)


def main():
    """
    function responsable for run streamlit app
    """
    st.title(body='Mann Kendall Solution')

    file_upload = st.sidebar.file_uploader(label="Upload Excel File",
                                           encoding=None,
                                           type=["xlsx", "xls"])

    if file_upload:

        results, df = cache_generate_mann_kendall(file_upload)

        st.sidebar.markdown(get_table_download_link(results),
                            unsafe_allow_html=True)

        page = st.sidebar.selectbox("2 - Choose a options",
                                    ["", "Online Plots"])
        st.write("Choose a option in left side")

        if page == "Online Plots":
            plot_online(results, df)
        elif page == "Export Plots":
            pass


@st.cache
def cache_generate_mann_kendall(file):
    return generate_mann_kendall(file.read())


def get_table_download_link(dataframe: pd.DataFrame):
    """
    Generate a button to download a file

    Arguments:
        dataframe {pd.DataFrame} -- dataframe wants download

    Returns:
        {str} -- html in string that create a button with href as stream
    """
    val = to_excel(dataframe)
    b64 = base64.b64encode(val)
    # TODO: Create a random number as filename, check generate_xlsx
    return ('<p style="text-align:center;">'
            f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
            'download="mann_kendall.xlsx">Download Excel file</a></p>')
    # decode b'abc' => abc)


def to_excel(dataframe: pd.DataFrame):
    """
    convert datafram to excel format and return it as byte

    Arguments:
        dataframe {pd.DataFrame} --  dataframe wants convert to excel format

    Returns:
        {bytes} -- excel file as  bytes
    """

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def plot_online(results, dataframe: pd.DataFrame):
    desired_wells = st.multiselect(
        'Select Well',
        results.Well.unique())

    if len(desired_wells):

        desired_component = get_desired_component(
            results, desired_wells)

        df_filtered = filter_well_component(
            dataframe, desired_wells, desired_component)
        df_filtered = df_filtered.dropna()
        # df_filtered = fillna(df_filtered, desired_component)

        name = ', '.join(desired_wells)

        f = px.line(
            df_filtered.reset_index(drop=True).fillna(method='pad'),
            x="Date", y=desired_component, color='well', log_y=True,
            title=f'{name} x {desired_component}',
            # width=300, height=600
        )

        st.plotly_chart(f, use_container_width=True)


def plots_export():
    pass


def get_desired_component(results: pd.DataFrame, desired_wells: list):
    results_filter_by_well = results[results.Well.isin(desired_wells)]
    desired_component = st.selectbox(
        "Select Component", results_filter_by_well.Analise.unique())
    return desired_component


def filter_well_component(df_transposed: pd.DataFrame,
                          desired_well: list, desired_component: str):

    df_filtered = df_transposed[df_transposed.well.isin(desired_well)]

    df_filtered = df_filtered[
        ['well', 'Date', desired_component]].sort_values('Date')
    df_filtered[desired_component] = df_filtered[
        desired_component].apply(float)
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def fillna(df_filtered: pd.DataFrame, component: str):
    df_concat = pd.DataFrame()
    for well in df_filtered.well.unique():
        df_temp = df_filtered.query(f"well=='{well}'").sort_values('Date')
        df_temp[component] = df_temp[component].fillna(method='ffill',
                                                       limit=1)
        df_concat = pd.concat([df_temp, df_concat])
    return df_concat


if __name__ == '__main__':
    main()
