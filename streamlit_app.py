import streamlit as st # pyright: ignore[reportMissingImports]
import time
from datetime import datetime, timezone, timedelta
from scripts import rhrrhead

if st.button("Back to Main Page"):
    if 'selected_district' in st.session_state:
        del st.session_state['selected_district']
    st.success("You will be redirected to Main Page soon")

st.button("Reload Data")

# Global Var Initialization
if 'selected_district' not in st.session_state:
    st.markdown("Location is not defined")
    time.sleep(1)
    st.switch_page("pages/welcome.py")

Header = st.empty()
Current_Weather = st.empty()

cwr = rhrrhead.Current_Weather_Report()
for i in range(0, 101, 50):
    match i:
        case 0:
            message = "Fetching Weather Data..."
        case 50:
            cwr.fetch_data()
            message = "Retreiving Weather Data"
        case 100:
            message = "Wait for it..."
        case _:
            message = "Error"
    Header.progress(i, message)
    time.sleep(1)

st.markdown("""
    <style>
        ul, li{
            list-style-type: none;
        }
    </style>
    """, unsafe_allow_html=True)

with Header.container():
    st.header(f"Weather Report at {st.session_state['selected_district']}")
    st.subheader('Time Information')
    current_datetime = datetime.now().astimezone(timezone(timedelta(hours=8)))
    st.markdown(f'<ul><li>{current_datetime.strftime("Today is %Y/%m/%d. <br>Current Time: %H:%M:%S")}</li></ul>', unsafe_allow_html=True)


cwr.update_user_data()
with Current_Weather.container():
    with st.empty():
        st.markdown(f"<h1>Lighting Information</h1><ul><li>{cwr.fetch_lighting()}</li></ul>" , unsafe_allow_html = True)
    with st.empty():
        st.markdown(f"<h1>UV Information</h1><ul><li>{cwr.fetch_uv()}</li></ul>" , unsafe_allow_html = True)
    with st.empty():
        st.markdown(f"<h1>Temperature Information</h1><ul><li>{cwr.fetch_temperature()}</li></ul>" , unsafe_allow_html = True)
    with st.empty():
        st.markdown(f"<h1>Humidity Information</h1><ul><li>{cwr.fetch_humidity()}</li></ul>" , unsafe_allow_html = True)
    with st.empty():
        st.markdown(f"<h1>Warning Information</h1><ul><li>{cwr.fetch_and_process_warning()}</li></ul>" , unsafe_allow_html = True)
    with st.empty():
        st.markdown(f"<h1>Special Message Information</h1><ul><li>{cwr.fetch_and_process_ultil()}</li></ul>" , unsafe_allow_html = True)

