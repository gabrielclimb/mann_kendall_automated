#!/usr/bin/env python
# utf-8

import base64
from io import BytesIO

import pydeck as pdk
import streamlit as st

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
            pass
        elif page == "Graphs":
            desired_well = st.selectbox("Select Well",
                                        results.Well.unique())
            if desired_well:
                results_filter_by_well = results.query(
                    f"Well=='{desired_well}'")
                desired_component = st.selectbox(
                    "Select Well", results_filter_by_well.Analise.unique())
#         if check_excel_structure(df):
#             kml = create_kml_from_excel(df)
#             map_plot(df)
#             st.write("")
#             st.markdown(get_kml_download_link(kml), unsafe_allow_html=True)


#     page = st.sidebar.selectbox("Escolha a página",
#                                 ["KML -> Excel", "Excel -> KML"])

#     st.write("Selecione a opção na esquerda")
#     if page == "KML -> Excel":
#         file_upload = st.sidebar.file_uploader(label="Upload Excel File",
#                                                encoding=None,
#                                                type=["kml"])
#         if file_upload is not None:
#             df = treat_kml(file_upload)
#             map_plot(df)
#             st.write("")
#             st.dataframe(df)
#             st.write("")
#             st.markdown(get_table_download_link(df), unsafe_allow_html=True)

#     elif page == "Excel -> KML":
#         st.write(
#             "O arquivo deve conter as colunas: nome, longitude e latitude")
#         file_upload = st.sidebar.file_uploader(label="Upload Excel",
#                                                encoding=None)

#         if file_upload is not None:
#             df = pd.read_excel(file_upload.read())
#             if check_excel_structure(df):
#                 kml = create_kml_from_excel(df)
#                 map_plot(df)
#                 st.write("")
#                 st.markdown(get_kml_download_link(kml), unsafe_allow_html=True)


@st.cache
def cache_generate_mann_kendall(file):
    return generate_mann_kendall(file.read())

# @st.cache
# def treat_kml(kml_file):
#     """[summary]
#     Arguments:
#         kml_file {[type]} -- [description]
#     Returns:
#         [type] -- [description]
#     """

#     root = objectify.fromstring(kml_file.read())

#     # getting name space
#     namespace = {"kml": root.xpath("/*")[0].nsmap[None]}

#     waypoint_folder_position = get_waypoint_folder_position(root, namespace)

#     name = root.xpath(
#         f"//kml:Folder[{waypoint_folder_position}]/"
#         "kml:Placemark/kml:name/text()",
#         namespaces=namespace
#     )

#     point = root.xpath(
#         f"//kml:Folder[{waypoint_folder_position}]/kml:Placemark/kml:Point/"
#         "kml:coordinates/text()",
#         namespaces=namespace
#     )

#     df = pd.DataFrame({'nome': name, 'point': point})
#     df.nome = df.nome.apply(str)
#     df.point = df.point.apply(str).str.split(",")
#     df['longitude'] = df.point.apply(lambda x: float(x[0]))
#     df['latitude'] = df.point.apply(lambda x: float(x[1]))
#     df['elevation'] = df.point.apply(lambda x: float(x[2]))
#     return df.drop(columns=['point'])

# def map_plot(df):
#     """[summary]
#     Arguments:
#         df {[type]} -- [description]
#     """
#     st.pydeck_chart(
#         pdk.Deck(
#             map_style="mapbox://styles/gabrielclimb/ckc5aihsj00l11jlflq8fssax",
#             # mapbox_key='pk.eyJ1IjoiZ2FicmllbGNsaW1iIiwiYSI6ImNqbTZlOXdsbjFhMXMzcG4yamp6YTg4aGgifQ.RIuQUZv8WVNvNoVYdRVvXg',
#             initial_view_state=pdk.ViewState(
#                 latitude=df.latitude.values[0],
#                 longitude=df.longitude.values[0],
#                 zoom=15,
#                 pitch=0
#             ),
#             layers=[
#                 pdk.Layer(
#                     "ScatterplotLayer",
#                     data=df,
#                     get_position="[longitude, latitude]",
#                     get_radius=20,
#                     get_color='[200, 30, 0, 160]'
#                 )
#             ]
#         )
#     )


# def get_table_download_link(df):
#     """[summary]
#     Arguments:
#         df {[type]} -- [description]
#     Returns:
#         [type] -- [description]
#     """
#     val = to_excel(df)
#     b64 = base64.b64encode(val)  # val looks like b'...'
#     return ('<p style="text-align:center;">'
#             f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
#             'download="extract.xlsx">Download Excel file</a></p>')
#     # decode b'abc' => abc)


# def to_excel(df):
#     """[summary]
#     Arguments:
#         df {[type]} -- [description]
#     Returns:
#         [type] -- [description]
#     """
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False, sheet_name='Sheet1')
#     writer.save()
#     processed_data = output.getvalue()
#     return processed_data


# def get_kml_download_link(kml):
#     """[summary]
#     Arguments:
#         kml {[type]} -- [description]
#     Returns:
#         [type] -- [description]
#     """

#     val = bytes(kml, 'utf-8')
#     b64 = base64.b64encode(val)
#     return ('<p style="text-align:center;">'
#             f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
#             'download="extract.kml">Download KML file</a></p>')


if __name__ == '__main__':
    main()
