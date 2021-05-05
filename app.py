import streamlit as st
import pandas as pd
import numpy as np
from vaccine_availibility import Covictory


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")


st.write("""
# The Covictory App
This app gets vaccine availibility by state and district.
Developed by: Shankar Kumar
""")

st.subheader("State Details")
state_detail = st.text_input('Input your state name here:')

if state_detail:
    district_detail = st.text_input('Input your district name here:')
    cov_obj = Covictory(state_detail)
    cov_obj.initialize()
    if district_detail:                
        vac_df = cov_obj.get_vaccine_availibility(district_detail)
        #select only relevant columns
        vac_df = vac_df[["center_id", "name", "block_name", "district_name", "state_name", "pincode", "from", "to", "fee_type","date"]]    
        st.write(vac_df)
    else:
        st.write("Please enter district details!")
        # vac_df = cov_obj.get_vaccine_availibility("thane")  # default district
        # vac_df = vac_df[["center_id", "name", "block_name", "district_name", "state_name", "pincode", "from", "to", "fee_type","date"]]    
        # st.write(vac_df)
else:
    st.write("Please enter state and district details!")


