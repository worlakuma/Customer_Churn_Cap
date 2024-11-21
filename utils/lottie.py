import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie

# Create a function to load lottie data from with persistence across multiple pages at session-state
# @st.cache_data(show_spinner=False, persist=True)
# def load_lottie_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error(f'Invalid response from {url}')
#         return None

# @st.cache_data(show_spinner=False, persist=True)
# def load_lottie_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         try:
#             return response.json()
#         except json.JSONDecodeError:
#             st.error("Error decoding JSON.")
#             return None
#     else:
#         st.error(f"Invalid response from {url}")
#         return None

DEBUG = False  # Set to True for debugging locally

@st.cache_data(show_spinner=False, persist=True)
def load_lottie_data(url):
    response = requests.get(url)
    if DEBUG:
        st.write(f"URL: {url}, Status Code: {response.status_code}")
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("Error decoding JSON.")
            return None
    else:
        st.error(f"Invalid response from {url}")
        return None
    
# Display loaded lottie data on various pages
def display_lottie(page_name):
    lottie_urls = {
        'Homepage': "https://raw.githubusercontent.com/worlakuma/Customer_Churn_Cap/main/assets/Animation%20-%201730036148913.json",
        'Data': 'https://raw.githubusercontent.com/worlakuma/Customer_Churn_Cap/main/assets/Animation%20-%201723456654279.json',
        }
    url = lottie_urls.get(page_name)
    if url:
        animation_data = load_lottie_data(url)
        if animation_data:
            st_lottie(animation_data, height=300, key=page_name)  
        else:
            st.error(f"No lottie animation data available for {page_name}")
    else:
        st.error("Invalid or missing URL for this page.")
    