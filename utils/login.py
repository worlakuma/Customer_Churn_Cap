# import streamlit as st
# import yaml
# from yaml.loader import SafeLoader
# import streamlit_authenticator as stauth
# from streamlit_authenticator.utilities import LoginError

# # Load configuration file
# def load_config(file_path):
#     with open(file_path, 'r') as file:
#         config = yaml.load(file, Loader=SafeLoader)
#     return config

# # config_file = 'config.yaml'
# # config = load_config(config_file)

# # authenticator = stauth.Authenticate(
# #     config['credentials'],
# #     config['cookie']['name'],
# #     config['cookie']['key'],
# #     config['cookie']['expiry_days'],
# #     config['preauthorized']
# # )

# # Create authentication object
# def initialize_auth(config):
#     if 'authenticator' not in st.session_state:
#         st.session_state['authenticator'] = stauth.Authenticate(
#             config['credentials'],
#             config['cookie']['name'],
#             config['cookie']['key'],
#             config['cookie']['expiry_days'],
#             config.get('preauthorized', {}),
#             # False
#         )
#     return st.session_state['authenticator']    

# # Render the login widget
# # name, authentication_status, username = authenticator.login()

# # Invoke the login authentication
# def invoke_login_widget(page_title):
#     config_file = './config.yaml'
#     config = load_config(config_file)
#     authenticator = initialize_auth(config)

# if not st.session_state('authentication_status', False):
#     st.title('Login')
#     try:
#         authenticator.login('sidebar', 'Login')
#     except LoginError as e:
#         st.error(e)    
# if st.session_state('authentication_status'):
#     if page_title == 'Homepage':


# Update authentication status in session state
# if st.session_state['authentication_status'] == None:
#     st.warning('Please key in your username and password')
# elif st.session_state['authentication_status'] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state['authentication_status']:
#     # st.write(f'Welcome *{name}*')
#     st.markdown('Explore the data, dashboard and predictions pages for prompt and accurate churn forecast')
#     authenticator.logout('Logout', 'sidebar')

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
            config.get('preauthorized', {})  # Use get to avoid missing key errors
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
            # Invoke the login widget
            # name, authentication_status, username = authenticator.login('sidebar', 'Login')
            authenticator.login('main', 'Login')
            # if authentication_status:
            #     st.session_state['authentication_status'] = True
            #     st.session_state['username'] = username
            #     st.success(f"Welcome {name}")
            # elif authentication_status == False:
            #     st.error('Username/password is incorrect')
            # else:
            #     st.info('Please enter your credentials')
        
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
