import pandas as pd
import streamlit as st
import numpy as np
import time
# import folium

# if inaccurate  , it will show on map with tooltip, inaccurate location

empty_header = st.empty()
with empty_header:
    st.header("Reading_map")
    time.sleep(0.5)
map_data = pd.read_csv('Weather_Station_Rainfall.csv', index_col = False)

district = list(map_data['District'].unique())
with empty_header:
    st.header("")
def filter_map(selected_district: str):
    # return filtered data
    unstructured_df = map_data[map_data['District'] == selected_district]
    unstructured_df['Latitude_dec'], unstructured_df['Longitude_dec'] = lat_in_dec(unstructured_df['Lat_deg'], unstructured_df['Lat_min'], unstructured_df['Lat_sec']), lat_in_dec(unstructured_df['Lon_deg'], unstructured_df['Lon_min'], unstructured_df['Lon_sec'])
    unstructured_df['Weather Station(alternative)'] = np.where(
        unstructured_df['Nearest LandMark'].notna() & (unstructured_df['Nearest LandMark'] != ''),
        unstructured_df['Weather Station'] + '(' + unstructured_df['Nearest LandMark'] + ')',
        unstructured_df['Weather Station']
    )
    return unstructured_df[['Weather Station', 'Weather Station(alternative)', 'Latitude_dec', 'Longitude_dec', 'Weather Station Location']]

def lat_in_dec(deg:int, m:int, s:int):
    if deg is None or m is None or s is None:  # just a redundant function
        msg = "degrees" if deg is None else "minutes" if m is None else "seconds"
        print(f"{msg} is None, check your code")
        return 0
    return deg + m / 60.0 + s / 3600.0