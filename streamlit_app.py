import streamlit as st
import time
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
    DAY_Weather_types = ["rain_cloud", "sun_behind_rain_cloud", 
                    "partly_sunny_rain", "sun_behind_cloud",
                    "barely_sunny", "sun_small_cloud", 
                    "mostly_sunny", "sunny"]
    NIGHT_Weather_types = []
    Current_Weather_types = DAY_Weather_types[-2]
    st.header(f":{Current_Weather_types}: Weather Report in {Current_district}")

    st.write(f"{Current_district} is {Current_Weather_types.replace('_', ' ')} today")

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
    
    #selected_district = st.selectbox("Please select your district below", Districts, accept_new_options = True)
    selected_district = "Tuen Mun"
    
    if st.button(f"Check Weather of {selected_district}"):
        st.session_state.district = selected_district
        st.session_state.report = True
        st.rerun()
    
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
                st.success('''Verification Sucess. 
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
