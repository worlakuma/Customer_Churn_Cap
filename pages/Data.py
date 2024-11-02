import requests
from streamlit_lottie import st_lottie
import streamlit as st
import pandas as pd
import time
import streamlit_authenticator as stauth
from utils.login import invoke_login_widget
from utils.lottie import display_lottie
import gdown

# Invoke the login form
invoke_login_widget('Data Hub')

# Fetch the authenticator from session state
authenticator = st.session_state.get('authenticator')

if not authenticator:
    st.error("Authenticator not found. Please check the configuration.")
    st.stop()

# Check authentication status
if st.session_state.get("authentication_status"):

    
    # Display the content in Streamlit
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("""
                            This page is desinged to provide users with a comprehensive and interactive interface for accessing and managing data.    
                                """)
            st.markdown(""" 
                            #### Upon uploading the data, users have access to several features:
                            
                            - #### Data Template: A sample template is provided to guide users in structuring their data correctly.
                            - #### Data View: This section provides the option to view the data either as numerical, categorical or combined data types 
                            - #### Data Summary: This section gives an overview of the dataset with key statistics
                            - #### Data Upload: This section provides the option to upload custom data for analysis 
                            """)
        with right_column:
            display_lottie('Data')                

    # Load the data
    @st.cache_data(persist=True)
    def load_data():
        df_train = pd.read_csv('./data/CAP_dash_upload.csv')
        return df_train         
    
    default_df = load_data()
    
    # Group various datatypes accordingly
    num_cols = default_df.select_dtypes('number').columns
    cat_cols = default_df.select_dtypes('object').columns
    

# Create progress bar to show the results of loading
    loadings_progress = st.progress(0)
    for i in range(100):
        loadings_progress.progress(i)
        time.sleep(0.03)
        loadings_progress.progress(i+1)

    st.success('Template data loaded successfully') 

   

# Create two columns options to display summary statistics for numerical and categorical features
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Summary Statistics**: Categorical Columns')
        st.dataframe(default_df[cat_cols].describe())
    with col2:
        st.write('**Summary Statistics**: Numerical Columns')
        st.dataframe(default_df[num_cols].describe())


    # Create two columns options to display datasets
    col1, col2 = st.columns(2) 
    with col1:
        options = st.selectbox(
             'Data view options',
             ("All data", "Numerical columns", "Categorical columns", "Column Description"),
            index=None,
            placeholder="Select view method...",)
# Conditionally display data based on the selected option
    if options == "All data":
        st.write("### All Data")    
        st.dataframe(default_df)

    elif options == "Numerical columns":
        st.write("### Numerical Columns")
        num_cols = default_df.select_dtypes("number").columns
        st.dataframe(default_df[num_cols])

    elif options == "Categorical columns":
        st.write("### Categorical Columns")
        cat_cols = default_df.select_dtypes("object").columns
        st.dataframe(default_df[cat_cols])

    elif options == "Column Description": 
        st.markdown(""" ####
                        This section provides a detailed description of the coluums in the dataset to assist users understand their data. `Note:` The variable CHURN is the target variable for prediction therefore not part of the described dataset below.
                    """) 
        # Create the DataFrame
        df_info = pd.DataFrame({"Column": default_df.columns, "Type": default_df.dtypes}) 

        # Map dtype values to more descriptive terms
        df_info['Type'] = df_info['Type'].replace({
                    'object': 'Categorical',
                    'int64': 'Numerical',
                    'float64': 'Numerical'
                })

                # Delete rows where 'Column' contains 'CHURN'
        df_info = df_info[~df_info['Column'].str.contains('CHURN', na=False)]

                # Reset the index after deletion
        df_info = df_info.reset_index(drop=True)

                # Set the index to start from 1
        df_info.index = df_info.index + 1

                # Display the table
        st.table(df_info)
        # Create a description dictionary for the expected features
        descriptions = {
                    'user_id': 'Unique identifier for each client',
                    'REGION': 'The location of each client',
                    'TENURE': 'Duration in the network (months)',
                    'MONTANT': 'Top-up amount',
                    'FREQUENCE_RECH': 'Number of times the customer refilled',
                    'REVENUE': 'Monthly income of each client',
                    'ARPU_SEGMENT': 'Income over 90 days / 3',
                    'FREQUENCE': 'Number of times the client has made an income',
                    'DATA_VOLUME': 'Number of connections',
                    'ON_NET': 'Inter expresso call',
                    'ORANGE': 'Call to Orange',
                    'TIGO': 'Call to Tigo',
                    'ZONE1': 'Call to zones1',
                    'ZONE2': 'Call to zones2',
                    'MRG': 'A client who is going',
                    'REGULARITY': 'Number of times the client is active for 90 days',
                    'TOP_PACK': 'The most active packs',
                    'FREQ_TOP_PACK': 'Number of times the client has activated the top pack packages',
                }   

        for col, desc in descriptions.items():
                    st.write(f"- *{col}*: {desc}")


# Sidebar for data upload
    st.sidebar.header("Data Upload")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
    st.sidebar.markdown(
            """
            **Note:** The uploaded CSV or Excel file should have the following columns:
            - `user_id`
            - `REGION`
            - `TENURE`
            - `MONTANT`
            - `FREQUENCE_RECH`
            - `REVENUE`
            - `ARPU_SEGMENT`
            - `FREQUENCE`
            - `DATA_VOLUME`
            - `ON_NET`
            - `ORANGE`
            - `TIGO`
            - `REGULARITY`
            - `TOP_PACK`
            - `FREQ_TOP_PACK`
            - `CHURN`
            """
        )

# Function to upload customer data
    @st.cache_data(persist=True)
    def load_uploaded_data(uploaded_file):
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)
                return df
            except Exception as e:
                st.error(f"Error: {e}")
                return None
        return None
    dfu = load_uploaded_data(uploaded_file)
    # if dfu is not None:
# Function to check if the upload data structure matches the default data structure
    def check_data_structure(uploaded_df, template_df):
        # Define a function to map the data types to their corresponding dtypes
        def standardize_data_type(df):
            dtype_mapping = {
                'float64': 'Numerical',
                'int64': 'Numerical',
                'object': 'Categorical',
                'category': 'Categorical'
            }
            return df.dtypes.map(lambda x: dtype_mapping.get(str(x), x)).tolist()
        # Compare column names to their corresponding dataframe names
        if list(uploaded_df.columns) != list(template_df.columns):
            return False
        
        if standardize_data_type(uploaded_df) != standardize_data_type(template_df):
            st.write("Uploaded DataFrame Dtypes:", uploaded_df.dtypes.tolist())
            st.write("Template DataFrame Dtypes:", template_df.dtypes.tolist())
            return False
        
        return True
    
    # Check if a file has been uploaded and perform structure check
    if dfu is not None and not dfu.empty:
        dfupdate = check_data_structure(dfu, default_df)
        
        # For uploaded data, ensure a different key for the second selectbox
        if dfupdate:
            st.success("Uploaded data structure matches the template.")
            st.dataframe(dfu)
            
            # Create two columns options to display datasets
            col1, col2 = st.columns(2) 
            with col2:
                options2 = st.selectbox(
                    'Data view options (Uploaded Data)',
                    ("All data", "Numerical columns", "Categorical columns", "Summary Statistics(Categorical Columns)", "Summary Statistics(Numerical Columns)"),
                    index=None,
                    placeholder="Select view method...",
                    key="uploaded_data_view"  # Assign a unique key here
                )
            
            # Conditionally display data based on the selected option
            if options2 == "All data":
                st.write("### All Data")    
                st.dataframe(dfu)

            elif options2 == "Numerical columns":
                st.write("### Numerical Columns")
                num_cols_uploaded = dfu.select_dtypes("number").columns
                st.dataframe(dfu[num_cols_uploaded])

            elif options2 == "Categorical columns":
                st.write("### Categorical Columns")
                cat_cols_uploaded = dfu.select_dtypes("object").columns
                st.dataframe(dfu[cat_cols_uploaded])

            elif options2 == "Summary Statistics(Categorical Columns)":
                st.dataframe(dfu[cat_cols].describe())

            elif options2 == "Summary Statistics(Numerical Columns)":
                st.dataframe(dfu[num_cols].describe())    
                    # Optionally display the uploaded DataFrame
        else:
            st.error("Uploaded data structure does not match the template.")
    else:
        st.info("Please upload a CSV or Excel file to check its structure.")

    