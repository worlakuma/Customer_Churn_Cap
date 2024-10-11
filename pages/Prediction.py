import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import os
from utils.login import invoke_login_widget

# Invoke the login form
invoke_login_widget('Future Projections')

# Fetch the authenticator from session state
authenticator = st.session_state.get('authenticator')

if not authenticator:
    st.error("Authenticator not found. Please check the configuration.")
    st.stop()

# Check authentication status
if st.session_state.get("authentication_status"):
    st.title("Predictive Analytics")


    # Load models
    @st.cache_resource(show_spinner='Models Loading')
    def models():
        rf_model = joblib.load('./Model_compartment/RF.joblib')
        knn_model = joblib.load('./Model_compartment/KNN.joblib')
        fnn_model = joblib.load('./Model_compartment/FNN.joblib')
        return rf_model, knn_model, fnn_model

    RF, KNN, FNN = models()

    # Initialize session state for selected model
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'Random Forest'

    # Select model 
    col1, col2 = st.columns(2)
    with col1:
        selected_model = st.selectbox('Select a Model', options=['Random Forest', 'K-Nearest Neighbors', 'Feedforward Neural Network'], 
                                    key='selected_model',
                                    index=['Random Forest', 'K-Nearest Neighbors', 'Feedforward Neural Network'].index(st.session_state.selected_model))
    
    # Get the selected model
    @st.cache_resource(show_spinner='Loading models...')
    def get_model(selected_model):
        if selected_model == 'Random Forest':
            pipeline = RF
        elif selected_model == 'K-Nearest Neighbors':
            pipeline = KNN
        else:
            pipeline = FNN
        encoder = joblib.load('./Model_compartment/encoder.joblib')
        return pipeline, encoder  

    # Initialize session state for predictions and probabilities
    if 'prediction' not in st.session_state:
        st.session_state['prediction'] = None
    if 'probability' not in st.session_state:
        st.session_state['probability'] = None

    # Prediction function
    def make_prediction(pipeline, encoder):
        # Collect user input from session state
 
        user_input = {
            'REGION': st.session_state['REGION'],
            'TENURE': st.session_state['TENURE'],
            'MONTANT': st.session_state['MONTANT'],
            'FREQUENCE_RECH': st.session_state['FREQUENCE_RECH'],
            'REVENUE': st.session_state['REVENUE'],
            'ARPU_SEGMENT': st.session_state['ARPU_SEGMENT'],
            'FREQUENCE': st.session_state['FREQUENCE'],
            'DATA_VOLUME': st.session_state['DATA_VOLUME'],
            'ON_NET': st.session_state['ON_NET'],
            'ORANGE': st.session_state['ORANGE'],
            'TIGO': st.session_state['TIGO'],
            'REGULARITY': st.session_state['REGULARITY'],
            'TOP_PACK': st.session_state['TOP_PACK'],
            'FREQ_TOP_PACK': st.session_state['FREQ_TOP_PACK'],
            }

        # Convert the input data to a DataFrame
        df = pd.DataFrame(user_input, index=[0])   
        
        # Make predictions
        pred = pipeline.predict(df) 
        pred_int = int(pred[0])   
        prediction = encoder.inverse_transform([[pred_int]])[0]

        # Calculate the probability of churn
        probability = pipeline.predict_proba(df)
        prediction_labels = "Churn" if pred == 1 else "No Churn"

        st.write(f'Predicted Churn: {prediction_labels}')
        
        # Update the session state with the prediction and probabilities
        st.session_state['prediction'] = prediction
        st.session_state['probability'] = probability
        st.session_state['prediction_labels'] = prediction_labels

        # Copy the original dataframe to the new dataframe
        hist_df = df.copy()
        hist_df['PredictionTime'] = datetime.date.today()
        hist_df['ModelUsed'] = st.session_state['selected_model']
        hist_df['Prediction'] = prediction
        hist_df['Probability'] = np.where(pred == 1, np.round(probability[:, 1] * 100, 2), np.round(probability[:, 0] * 100, 2))
        
        # Save the history dataframe to a CSV file
        hist_df.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

        return prediction, probability, prediction_labels

    def get_user_input():
        pipeline, encoder = get_model(selected_model)

        with st.form('input-feature', clear_on_submit=True):
   
                st.write('### Subscriber Account Details')
                st.selectbox('Region', options=['DAKAR', 'SAINT-LOUIS', 'THIES', 'LOUGA', 'MATAM', 'FATICK', 'KAFFRINE','KAOLACK', 'KEDOUGOU', 'KOLDA', 'DIOURBEL', 'SEDHIOU', 'TAMBACOUNDA', 'ZIGUINCHOR'], key='REGION')
                st.selectbox('Key in Tenure', options=['D3-6 month', 'E6-9 month', 'F9-12 month', 'G12-15 month', 'H15-18 month', 'I18-21 month', 'J21-24 month', 'K>24 month'], key='TENURE')
                st.number_input('Key in Top-up Amount/montant', min_value=0.00, max_value=1000000.00, step=0.10, key='MONTANT')
                st.number_input('Key in Frequency of Top-up', min_value=0.00, max_value=500.00, step=0.10, key='FREQUENCE_RECH')
                st.number_input('Key in Monthly Revenue per Customer', min_value=0.00, max_value=1000000.00, step=0.10, key='REVENUE')
                st.number_input('Key in Customer Income over the 90 day period', min_value=0.00, max_value=1000000.00, step=0.10, key='ARPU_SEGMENT')
                st.number_input('Key in Frequency of Income over the 90 day period', min_value=0.00, max_value=200.00, step=0.10, key='FREQUENCE')
                st.number_input('Enter Data Volume', min_value=0.00, max_value=1000000.00, step=0.10, key='DATA_VOLUME')
                st.number_input('Enter Number Calls made within the same network', min_value=0.00, max_value=100000.00, step=0.10, key='ON_NET')
                st.number_input('Enter Number of Calls to Orange', min_value=0.00, max_value=100000.00, step=0.10, key='ORANGE')
                st.number_input('Enter Number of Calls to Tigo', min_value=0.00, max_value=100000.00, step=0.10, key='TIGO')
                st.number_input('Enter Number of times Customer is Active over the 90 period', min_value=0.00, max_value=100.00, step=0.10, key='REGULARITY')
                st.selectbox('Enter Most Active Package', options=['Data package', 'Voice Package', 'IVR Package', 'Twitter Package', 'Facebook Package', 'EVR Package', 'EVC Package', 'Jokko Package', 'Pilot Package', 'CVM Package', 'GPRS Package', 'Combo Package', 'Subscribtion Package'], key='TOP_PACK')
                st.number_input('Enter Number of times Customer activated the Top Package', min_value=0.00, max_value=1000.00, step=1.00, key='FREQ_TOP_PACK')
                st.form_submit_button('Make Prediction', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))
            
    get_user_input()

    # Display prediction results
    prediction = st.session_state['prediction']
    probability = st.session_state['probability']

    if prediction is None:
        st.markdown('### Prediction will show here')
    elif prediction == "YES":
        probability_of_yes = probability[0][1] * 100
        st.markdown(f'### The employee will leave the company with a probability of {round(probability_of_yes, 2)}%')
    else:
        # prediction == "NO",
        probability_of_no = probability[0][0] * 100
        st.markdown(f'### The employee will not leave the company with a probability of {round(probability_of_no, 2)}%')

    # Sidebar for Bulk prediction input
    st.sidebar.header("Input for Bulk Prediction")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file for prediction", type=["csv", "xlsx"])
    st.sidebar.markdown(
            """
            **Note:** The uploaded CSV or Excel file should have the following columns:
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
            """
        )
    def load_data(uploaded_file):
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    dfp = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    dfp = pd.read_excel(uploaded_file)
                return dfp
            except Exception as e:
                st.error(f"Error: {e}")
                return None
        else:
            return None

    dfp = load_data(uploaded_file)

    if dfp is not None:
        st.dataframe(dfp.head(3))
        if st.button("Predict on Uploaded Dataset"):
            pipeline, encoder = get_model(selected_model)
            
                   
            # Drop 'customerID' column
            dfp = dfp.drop('user_id', axis=1)

            # Drop other unwanted columns
            dfp = dfp.drop(['MRG', 'ZONE1', 'ZONE2'], axis=1)
                                  
            # Identify object columns to convert to category datatype
            object_columns_to_convert = dfp.select_dtypes(include=['object']).columns
            
            # Convert object columns to category datatype
            dfp[object_columns_to_convert] = dfp[object_columns_to_convert].astype('category')
            
            # Make predictions
            predictions = pipeline.predict(dfp)
            probabilities = pipeline.predict_proba(dfp)
            prediction_labels = encoder.inverse_transform(predictions)
            dfp['Predicted Churn'] = prediction_labels
            
            # Update the session state with the prediction and probabilities
            st.session_state['predictions'] = predictions
            st.session_state['probability'] = probabilities
            st.session_state['prediction_labels'] = prediction_labels

                # Copy the original dataframe to the new dataframe
            his_df = dfp.copy()
            his_df['PredictionTime'] = datetime.date.today()
            his_df['ModelUsed'] = st.session_state['selected_model']
            his_df['Prediction'] = predictions
            his_df['Probability'] = np.where(predictions == 1, np.round(probabilities[:, 1] * 100, 2), np.round(probabilities[:, 0] * 100, 2))
        
            # Save the history dataframe to a CSV file
            # his_df.to_csv('./data/History.csv', mode='a', header=not os.path.exists('./data/History.csv'), index=False)            
            #Display the predictions
            # st.dataframe(dfp)
            st.dataframe(his_df)
        
       