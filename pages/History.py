import requests
from streamlit_lottie import st_lottie
import streamlit as st
from utils.login import invoke_login_widget
# from utils.lottie import display_lottie_on_page
import pandas as pd
import plotly.express as px
import joblib
import os

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

    # # Historical Analysis Section
    # st.subheader("Historical Trends Analysis")
    # st.write("This section visualizes key trends over time, highlighting customer behavior and revenue generation.")

    # # Sample Visualization: Revenue over time (even without dates, can use index or other columns)
    # if 'Revenue' in data.columns:
    #     fig1 = px.line(data, x=data.index, y='Revenue', title='Revenue Over Time', labels={'x': 'Index', 'Revenue': 'Revenue'})
    #     st.plotly_chart(fig1, use_container_width=True)

    # # Additional Visualizations
    # if 'CustomerSegment' in data.columns:
    #     customer_segment_counts = data['CustomerSegment'].value_counts().reset_index()
    #     customer_segment_counts.columns = ['Customer Segment', 'Count']
    #     fig2 = px.bar(customer_segment_counts, x='Customer Segment', y='Count', title='Customer Segmentation Distribution')
    #     st.plotly_chart(fig2, use_container_width=True)

    # st.write("---")



    # # Replace with an existing Lottie animation URL
    # lottie_history = "https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json" 

    # st_lottie(lottie_history, height=300, key="history")
