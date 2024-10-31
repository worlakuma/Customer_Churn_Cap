import requests
from streamlit_lottie import st_lottie
import streamlit as st
from utils.login import invoke_login_widget
import pandas as pd
import plotly.express as px


# Invoke the login form
invoke_login_widget('Historical Insights')

# Fetch the authenticator from session state
authenticator = st.session_state.get('authenticator')

if not authenticator:
    st.error("Authenticator not found. Please check the configuration.")
    st.stop()

# Check authentication status
if st.session_state.get("authentication_status"):

    # Business Insights Section
    st.subheader("This section provides all previous single predictions.")

    # Load Historical Data (Assuming a CSV without dates)
    data = pd.read_csv('./data/history.csv') # Replace with your

    st.dataframe(data) 
