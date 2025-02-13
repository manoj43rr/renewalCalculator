import streamlit as st
import pages.home as home
import pages.incentive_calc as incentive_calc
import pages.analysis as analysis

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Annual Incentive Calculator", "Non Annual Incentive Calculator"])


if page == "Home":
    home.app()
elif page == "Incentive Calculator":
    annual_incentive_calc.app()
elif page == "Data Analysis":
    non_annual_incentive_calc.app()
    
