#!/usr/bin/env python
# utf-8

import streamlit as st
import plotly.express as px

from mann_kendall_automated.generate import generate_mann_kendall


def main():
    """
    function responsable for run streamlit app
    """
    st.header(body='Mann Kendall Solution')

    file_upload = st.sidebar.file_uploader(label="Upload Excel File",
                                           encoding=None)

    if file_upload is not None:
        results, df = cache_generate_mann_kendall(file_upload)
        # st.dataframe(results)
        page = st.sidebar.selectbox("Choose a options",
                                    ["Export", "Graphs"])
        st.write("Choose a option in left side")

        if page == "Export":
            export_option(results, df)
        elif page == "Graphs":
            graphs_option(results, df)

@st.cache
def cache_generate_mann_kendall(file):
    return generate_mann_kendall(file.read())


def export_option(results, df):
    print('Troxa')


def graphs_option(results, df):
    desired_well = st.selectbox("Select Well",
                                results.Well.unique())
    if desired_well:

        desired_component = get_desired_component(
            results, desired_well)

        df_filtered = filter_well_component(
            df, desired_well, desired_component)

        st.dataframe(df_filtered.reset_index(drop=True))

        f = px.line(df_filtered,
                    x="Date", y=desired_component,
                    title=f'{desired_well} x {desired_component}')

        st.plotly_chart(f, use_container_width=True)


def get_desired_component(results, desired_well):
    results_filter_by_well = results.query(
        f"Well=='{desired_well}'")
    desired_component = st.selectbox(
        "Select Well", results_filter_by_well.Analise.unique())
    return desired_component


def filter_well_component(df_transposed, desired_well, desired_component):

    df_filtered = df_transposed.query(f"well=='{desired_well}'")[
        ['Date', desired_component]].sort_values('Date')
    df_filtered[desired_component] = df_filtered[
        desired_component].apply(float)
    df_filtered = df_filtered.reset_index(drop=True)

    return df_filtered


if __name__ == '__main__':
    main()
