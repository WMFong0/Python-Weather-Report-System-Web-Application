import streamlit as st
import pandas as pd
from scripts import map_script

st.session_state['selected_district','selected_weather_station'] = None
st.set_page_config(
    layout="wide"
)

def gen_map():
    if st.session_state['selected_district'] is None:
        return
    st.write("If you can't see any marker on the map, please refresh the page.")
    cur_map = map_script.filter_map(st.session_state['selected_district'])
    st.write(cur_map)
    with st.container():
        import folium
        from streamlit_folium import st_folium

        number_of_station = len(cur_map)
        if number_of_station == 1:
            m = folium.Map(location=[cur_map['Latitude_dec'], cur_map['Longitude_dec']], zoom_start=15)
        else:
            lat_centre, lon_centre = cur_map['Latitude_dec'].sum()/number_of_station, cur_map['Longitude_dec'].sum()/number_of_station
            # Add better bounding LATER
            m = folium.Map(location=[lat_centre, lon_centre], zoom_start=10)
        for index, row in cur_map.iterrows():
            folium.Marker(
                [row['Latitude_dec'], row['Longitude_dec']], popup=row['Weather Station(alternative)'] + " Weather Station", tooltip=row['Weather Station Location']
            ).add_to(m)
        
        st.write("Weather Station Map")
        st_data = st_folium(m, width=725)
        st.session_state['selected_weather_station'] = st.selectbox("Pick a weather station.", [None] + list(cur_map['Weather Station']))

st.markdown("<br> Welcome Using Weather Report System.<br>All weather data credits back to Hong Kong Observatory", unsafe_allow_html=True, width="stretch")
st.session_state['selected_district'] = st.selectbox("Where you at?", [None] + list(map_script.district))

gen_map()

st.button(label="Reload Map", disabled=(st.session_state['selected_district'] is None), on_click=gen_map)
if st.button(label="Click me to enter Data Page", disabled=(st.session_state['selected_district'] is None)):
    st.session_state['selected_district'] = st.session_state['selected_district']
    st.switch_page("streamlit_app.py")
