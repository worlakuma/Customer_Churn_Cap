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

    st.title("Company History")

    # Display the history page content
    # with st.container():
    #     st.write("---")
        
    #     left_column, right_column = st.columns(2)

    #     with left_column:
    #         st.header("Our Journey")
    #         st.write(
    #             """
    #             Our company has been at the forefront of innovation for over a decade.
    #             Here’s a look at some of the milestones we’ve achieved along the way.
    #             """
    #         )
    #         st.subheader("Milestones")
    #         st.markdown(
    #             """
    #             - **2009:** Founded with the mission to revolutionize the tech industry.
    #             - **2012:** Launched our first major product.
    #             - **2015:** Expanded internationally.
    #             - **2020:** Surpassed 10 million users.
    #             - **2023:** Named one of the most innovative companies in the world.
    #             """
    #         )
    #     with right_column:
    #         display_lottie_on_page("Historical Insights")

    # st.write("---")

    # Business Insights Section
    st.subheader("Business Insights")
    st.write("This section provides actionable insights derived from customer data analysis to help identify key trends, behaviors, and opportunities for growth.")

    # Load Historical Data (Assuming a CSV without dates)
    
    data = pd.read_csv('./data/history.csv') # Replace with your

    st.dataframe(data) # Replace with your actual data path

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
