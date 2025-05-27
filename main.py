import streamlit as st
from geocode import get_geocoded_df
import pandas as pd
from streamlit_folium import st_folium
from map import generate_heatmap, generate_preview
import os
from utils import AppState, detect_header_row, save_markers

st.set_page_config(layout="wide")

tabs = st.tabs(['Upload & Select', 'Geocoding', 'Map'])
if 'app_state' not in st.session_state:
    st.session_state['app_state'] = AppState.UPLOADING

with tabs[0]:
    st.title("Excel Column Selector")

    uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xls"])

    if uploaded_file:
        header_row = detect_header_row(uploaded_file)
        df = pd.read_excel(uploaded_file, header=header_row, index_col=False)
        df = df.dropna(axis=1, how='all')
        st.write("### 🔍 Preview of your data", df.head())

        columns = df.columns.tolist()
        empty_option = "-- Select --"
        column_options = [empty_option] + columns

        radio_columns = st.columns(4)
        with radio_columns[2]:
            state_mode = st.radio("🗺️ State source", ["Column", "Fixed"], horizontal=True)
        with radio_columns[3]:
            country_mode = st.radio("🌍 Country source", ["Column", "Fixed"], horizontal=True)

        with st.form(key='Dataframe Column Selection'):
            address_columns = st.columns(4)
            with address_columns[0]:
                address_column = st.selectbox("📍 Address", column_options)

            with address_columns[1]:
                city_column = st.selectbox("🏙️ City (optional)", column_options)

            with address_columns[2]:
                if state_mode == "Column":
                    state_column = st.selectbox("State column", column_options)
                else:
                    state = st.text_input("Fixed state")

            with address_columns[3]:
                if country_mode == "Column":
                    country_column = st.selectbox("Country column", column_options)
                else:
                    country = st.text_input("Fixed country")

            info_and_date_columns = st.columns(2)
            with info_and_date_columns[0]:
                date_column = st.selectbox("📆 Select the date column", column_options)

            with info_and_date_columns[1]:
                info_column = st.selectbox("ℹ️ Select the info column", column_options)

            submitted = st.form_submit_button('Process')

        if submitted:
            if address_column == empty_option or date_column == empty_option:
                st.error('You must select at least the address and date columns')
            else:
                fixed = {}
                column_names = {'address': address_column,
                           'date': date_column,
                           'info': info_column}
                if city_column != empty_option:
                    column_names['city'] = city_column
                if state_mode == 'Fixed':
                    fixed['state'] = state
                elif state_column != empty_option:
                    column_names['state'] = state_column
                if country_mode == 'Fixed':
                    fixed['country'] = country
                elif country_column != empty_option:
                    column_names['country'] = country_column
                st.session_state['app_state'] = AppState.GEOCODING
                st.session_state['df'] = df
                st.session_state['column_names'] = column_names
                st.session_state['fixed'] = fixed
                st.success("Switch to Geocoding Tab to fill any missing coordinates and preview them in the map")

with tabs[1]:
    st.header('Geocoding')
    if st.session_state['app_state'] == AppState.GEOCODING:
        with st.spinner('Getting coordinates'):
            geocoded_df = get_geocoded_df(st.session_state['df'],
                                          st.session_state['column_names'],
                                          st.session_state['fixed'])
        unresolved = geocoded_df[geocoded_df ['lat'].isna() | geocoded_df ['long'].isna()]
        if not unresolved.empty:
            with st.form('unresolved addresses'):
                st.markdown("### Addresses needing geocoding")
                fixed_unresolved = st.data_editor(unresolved, key="unresolved_editor")
                if st.form_submit_button('Save coordinates'):
                    if unresolved.isna().any().any():
                        st.error('Fill the missing coordinates')
                    else:
                        for idx in fixed_unresolved.index:
                            geocoded_df.loc[idx, 'lat'] = fixed_unresolved.loc[idx, 'lat']
                            geocoded_df.loc[idx, 'long'] = fixed_unresolved.loc[idx, 'long']
        else:
            st.session_state['app_state'] = AppState.PREVIEW
            st.session_state['df'] = geocoded_df
    if st.session_state['app_state'] == AppState.PREVIEW:
        m = generate_preview(st.session_state['df'])
        map_data = st_folium(m)
        if st.button('Save coordinates to database'):
            save_markers(st.session_state['df'])
            st.session_state['app_state'] = AppState.CREATING_MAP
    else:
        st.info("Upload a file first in the 'Upload & Select' tab.")


with tabs[2]:
    st.header("🗺️ Map Viewer")

    if st.session_state['app_state'] == AppState.CREATING_MAP:
        with st.spinner('Generating map'):
            generate_heatmap()
        with open('heatMap.html', 'r', encoding='utf-8') as f:
            html_map = f.read()
        st.components.v1.html(html_map, height=600)
    elif os.path.exists('heatMap.html'):
        with open('heatMap.html', 'r', encoding='utf-8') as f:
            html_map = f.read()
        st.components.v1.html(html_map, height=600)
    else:
        st.info("Upload a file and generate the map first in the 'Upload & Select' tab.")