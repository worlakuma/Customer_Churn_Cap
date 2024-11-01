
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import LoginError

# Load configuration file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

# Create authentication object
def initialize_auth(config):
    if 'authenticator' not in st.session_state:
        st.session_state['authenticator'] = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            # config.get('preauthorized', {})  # Use get to avoid missing key errors
        )
    return st.session_state['authenticator']

# Invoke the login authentication
def invoke_login_widget(page_title):
    config_file = './config.yaml'
    
    # Load the config file before passing it to initialize_auth
    config = load_config(config_file)
    
    authenticator = initialize_auth(config)
    
    if not st.session_state.get('authentication_status'):  # Use .get() for session state checks
        st.title('Login')
        try:
             authenticator.login('main', 'Login')
        except LoginError as e:
            st.error(e)
    else:
        st.title(page_title)

    if st.session_state.get('authentication_status'):
        if page_title == 'Homepage':
            st.sidebar.success('Welcome to our Homepage')
        elif page_title == 'Data':
            st.sidebar.success('Welcome to our Datahub')
        elif page_title == 'Predictions':
            st.sidebar.success('Predictions')   
        elif page_title == 'Dashboard':
            st.sidebar.success('Analytical Dashboard')
        elif page_title == 'History Page':
            st.sidebar.success('Historical Insights')    
    elif st.session_state.get == False:
        st.error('Username/password is incorrect')
    else:
        st.info('Please enter your credentials')    
