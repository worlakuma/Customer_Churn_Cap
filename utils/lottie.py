import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Create a function to load lottie data from with persistence across multiple pages at session-state
@st.cache_data(show_spinner=False, persist=True)
def load_lottie_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Invalid response from {url}')
        return None
    
# Display loaded lottie data on various pages
def display_lottie(page_name):
    lottie_urls = {
        'Homepage': 'http://as',
        'Predictions': 'http://as',
        'Dashboard': 'http://'
    }
    if page_name in lottie_urls:
        animation_data = load_lottie_data(lottie_urls[page_name]) 
        if animation_data:
            st_lottie(animation_data, height=300, key=page_name)  
    else:
        st.error("No lottie animation data found")      
           