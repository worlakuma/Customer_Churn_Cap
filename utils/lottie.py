import streamlit as st
import json
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
        # 'Homepage': 'https://github.com/worlakuma/Customer_Churn_Cap/blob/main/assets/Animation%20-%201723455741266.json',
        # 'Dashboard': 'https://github.com/worlakuma/Customer_Churn_Cap/blob/main/assets/Animation%20-%201723456654279.json',
        # 'Data': 'https://github.com/worlakuma/Customer_Churn_Cap/blob/main/assets/Animation%20-%201730036148913.json',
        'Homepage': "https://lottie.host/9ef1b405-72ec-4ba9-be8b-96a034df19c6/YIcIu9NyJP.json",
        # 'Homepage': 'https://raw.githubusercontent.com/worlakuma/Customer_Churn_Cap/main/assets/Animation%20-%201723455741266.json',
        'Dashboard': 'https://raw.githubusercontent.com/worlakuma/Customer_Churn_Cap/main/assets/Animation%20-%201723456654279.json',
        # 'About Us': 'https://lottie.host/f3734960-8bd5-4e1e-94c7-57787a497ac7/dXSG'
        # 'Data': 'https://raw.githubusercontent.com/worlakuma/Customer_Churn_Cap/main/assets/Animation%20-%201730036148913.json',
        # 'History': 'http://',
        # 'Predictions': 'http://as'
        
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
    # if page_name in lottie_urls:
    #     animation_data = load_lottie_data(lottie_urls[page_name]) 
    #     if animation_data:
    #         st_lottie(animation_data, height=300, key=page_name)  
    # else:
    #     st.error("No lottie animation data found")      
           