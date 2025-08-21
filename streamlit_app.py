import streamlit as st
import time
import datetime
import requests
from utility import *  
from cwr import Current_Weather_Report
from Hourly_Rainfall import Hourly_Rainfall

# session_state init
if "role" not in st.session_state:
  st.session_state.role = "User"
if "district" not in st.session_state:
  st.session_state.district = None
if "report" not in st.session_state:
    st.session_state.report = False


Districts = [None, "Tuen Mun", "Tin Shui Wai", "Yuen Long"]

def Test_Page_Check_Weather():
    Current_district = st.session_state.district
    
    st.header(f"Weather Report in {Current_district}")
    
    current_datetime = datetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    st.write(current_datetime.strftime('Today is %Y/%m/%d. \nCurrent Time: %H:%M:%S'))
    
    rainfall = Hourly_Rainfall(Current_district)
    rainfall_messages = rainfall.fetch_bundle()
    for msg in rainfall_messages:
        st.write(msg)
    
    weather = Current_Weather_Report(Current_district)
    weather_messages = weather.fetch_bundle()
    for msg in weather_messages:
        st.write(msg)

def leave_blank_for_development():
    st.header(":red[Page under development]", divider='gray')
    st.markdown("This page is leave blank for future development")

def welcome():
    if "role" not in st.session_state:
        st.session_state.role = "User"
    if "district" not in st.session_state:
        st.session_state.district = None
    if "report" not in st.session_state:
        st.session_state.report = False
    if st.session_state.role == "Admin":
        st.markdown("Hello Admin, please select any district to debug.")
    st.write("Welcome using Weather Report System. <br>"
             "This system uses Hong Kong Observatory Data to report. ", unsafe_allow_html = True)
    
    selected_district = st.selectbox("Please select your district below", Districts)
    
    if st.button(f"Check Weather of {selected_district}" if selected_district != None else "Please select district first"):
        if selected_district != None:
            st.session_state.district = selected_district
            st.session_state.report = True
            st.rerun()
        else:
            with st.container():
                st.warning("Please select district first")
    
    
    col2 = st.container()
    if st.session_state.role == "User":
        with col2:
            if st.button("Log in as an Admin"):
                st.session_state.role = "Unverified_Admin"
                st.rerun()
    elif st.session_state.role == "Admin":
        with col2:
            if st.button("Log out"):
                st.session_state.role = "User"
                st.success("You have successfully log out.")
                time.sleep(1)
                st.rerun()
                
def Admin_login():
    def Login_Check(Username: str, Password: str):
        return Password == "12345678"

    def Logout():
        with st.spinner("Logging Out For you"):
            time.sleep(2)
        st.success("Done!")
        st.session_state.logged_in = False
        st.session_state.role = "User"
        st.rerun()

    def Test_Page_Admin():
        st.write("Hello Admin")
        if st.button("Logout"):
            Logout()

    if st.session_state.role == "Unverified_Admin":
        st.header(":rainbow[Admin Login Page]", divider='gray')

        Username = st.text_input(
            label="Username",
            placeholder="Username Here",
            label_visibility="collapsed",
        )
        Password = st.text_input(
            label="Password",
            placeholder="Password Here",
            label_visibility="collapsed",
            type="password"
        )

        if st.button("Login"):
            progress_text = "Verifying admin identity"
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            if Login_Check(Username, Password):
                st.session_state.role = "Admin"
                st.success('''Verification Success. 
                You will be directed back to the Main Page. 
                Select any district to check the weather and debug''')
                time.sleep(1)
                st.rerun()
            else:
                st.error("Verification Failed. Reason: Incorrect Username or password")

        if st.button("Back to Main"):
            st.session_state.role = "User"
            st.rerun()
if st.session_state.role in ["User", "Admin"]:
    if st.session_state.report:
        Test_Page_Check_Weather()
        st.write(f"Welcome to {st.session_state.district}")
        if st.button("Back to Main Menu"):
            st.session_state.report = False
            st.rerun()
    else: welcome()
elif st.session_state.role == "Unverified_Admin":
  Admin_login()
