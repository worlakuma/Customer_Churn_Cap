import streamlit as st
import requests
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.Image import QUAD, BILINEAR
import yaml
from yaml.loader import SafeLoader
from streamlit_lottie import st_lottie
from streamlit_authenticator.utilities import LoginError, RegisterError
from utils.lottie import display_lottie
from utils.login import invoke_login_widget
import streamlit.components.v1 as components
import time

st.set_page_config(
    page_title='Customer Churn Predictor', layout='wide'
)

# Import the YAML file
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# invoke_login_widget('Homepage')
# Create the authenticator object
if 'authenticator' not in st.session_state:
        st.session_state['authenticator'] = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            # config['preauthorized']
        )
authenticator = st.session_state['authenticator']

# Load the authentication configuration
if not st.session_state.get('authentication_status'):  # Use .get() for session state checks
    st.title('Welcome to the Churn Predictor App')
    invoke_login_widget('Login')
    
    st.code("""
            Guest Account
            Username: jsmith
            Password: abc""")
    
    
if st.session_state['authentication_status']:
    # Place authenticator.logout in the sidebar
    with st.sidebar:
        authenticator.logout("Logout")

    
    selected = option_menu(None, options=["Home", "About Us"], 
            icons=['house','gear'], 
            menu_icon="cast", default_index=0, orientation="horizontal")
    selected
        
    if selected == "Home":

    # Display the content in Streamlit
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)

            with left_column:
                st.header('Predictive Analytics')
                st.markdown(""" ### This app is designed to predict customer churn for telecomunications companies in the business of providing customers with airtime and mobile data bundles""")
                
                st.header('Key features')
                st.markdown("""
                - Real-time data analysis
                - Advanced machine learning algorithms for predicting customer churn
                - Customizable dashboards and reports
                """)

                st.header('Technologies used')
                st.markdown('''
                - Python (with libraries like pandas, scikit-learn, and streamlit)
                - Machine learning algorithms (e.g., Random Forest, K-Nrearest Neighbors, and Feedforward Neural Network)
                - Data visualization libraries (e.g., matplotlib, seaborn)
                ''')
            with right_column:
                display_lottie("Homepage")

    if selected == 'About Us':
        with st.container():
            st.write('---')
            left_column, right_column = st.columns(2)
            with left_column:
                st.header('About Us')
                st.subheader("""
                                We are a team of data scientist with a diverse portfolio of projects
                                """)
                st.markdown(""" 
                            #### The mission of the team is to provide insights from data that will drive business decisions through:
                            
                            - #### Data exploration to harness the most optimal binary classification models capable of providing a thorough understanding of customer behaviour.
                            - #### Determining the lifetime values of customers to the business
                            - #### Forecasting the likelyhood of customer churning
                            """) 
                st.subheader('Contact')
                st.markdown('''
                - [Gabriel K. Kuma](https://www.linkedin.com/in/gabrielkuma/)
                    ''')
            with right_column:
                display_lottie('Homepage')     
        