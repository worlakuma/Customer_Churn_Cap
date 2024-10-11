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
# Function to load lottie animations from URL

# invoke_login_widget('Secure Login')
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
            config['preauthorized']
        )
authenticator = st.session_state['authenticator']

# Load the authentication configuration
if not st.session_state.get('authentication_status'):  # Use .get() for session state checks
    # st.warning('Please enter your credentials')
    
    # st.title('Welcome to our Homepage')
    # left_column, right_column = st.columns(2)
    # with left_column:
    #     st.header("Secure Login")
    #     st.write('''

    #             Please enter your credentials
                 
    #              '''
    #     )
    # with right_column:
    st.title('Welcome to the Churn Predictor App')
    invoke_login_widget('Login')
    
        # display_lottie_on_page("Login")
    st.code("""
            Guest Account
            Username: jsmith
            Password: abc""")
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status']:
    
# if st.session_state.get("authentication_status"):
    authenticator.logout("Logout", "sidebar")
#     st.sidebar.title(f'Welcome *{st.session_state["name"]}*')    

    selected = option_menu(None, options=["Home", "About Us"], 
            icons=['house','gear'], 
            menu_icon="cast", default_index=0, orientation="horizontal")
    selected
        #intro talking about title 
    if selected == "Home":

    # Display the content in Streamlit
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)

            with left_column:
                st.header('Predictive Analytics')
                st.markdown(""" ### This app is designed to predict customer churn for telecomunications companies in the business of providing customers with airtime and mobile data bundles""")
                
            st.header('Key features')
            st.markdown('''
            - Real-time data analysis
            - Advanced machine learning algorithms for predicting customer churn
            - Customizable dashboards and reports
            ''')

            st.header('Technologies used')
            st.markdown('''
            - Python (with libraries like pandas, scikit-learn, and streamlit)
            - Machine learning algorithms (e.g., logistic regression, decision trees)
            - Data visualization libraries (e.g., matplotlib, seaborn)
            ''')

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
                            - #### Determining the livetime values of customers to the business
                            - #### Forecasting the likelyhood of customer churning
                            """)  
        