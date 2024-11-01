import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import altair as alt
from utils.lottie import display_lottie
from utils.login import invoke_login_widget
# from pages.Data import load_data

# Invoke the login form
invoke_login_widget('Analytics Dashboard')

# Fetch the authenticator from session state
authenticator = st.session_state.get('authenticator')

if not authenticator:
    st.error("Authenticator not found. Please check the configuration.")
    st.stop()

# Check authentication status
if st.session_state.get("authentication_status"):
    st.subheader('Customer Churn Dashboard')
    st.markdown('--------------------------------')

    # Load default data
    @st.cache_data(persist=True, show_spinner=False)
    def load_default_data():
        df = pd.read_csv('./data/clean_cap_data.csv')
        return df
           
    df_train = load_default_data()

     # Ensure 'data_source' is initialized in session state
    if 'data_source' not in st.session_state:
        st.session_state['data_source'] = 'initial'

    # Create a selectbox option for EDA and KPIs
    col1, col2 = st.columns(2)
    with col1:
        eda_kpi_options = ['Exploratory Data Analysis (EDA)', 'Key Performance Indicators (KPIs)']
        eda_kpi_selection = st.selectbox('Select Analysis  Options', eda_kpi_options)
        
        num_columns = df_train.select_dtypes(['int64', 'float64']).columns
   
    # Create a function to apply filters
    def apply_filters(df):
        slider_values = {}
        for column in num_columns:
            if df[column].dtype == 'int64':
                min_value = int(df[column].min())
                max_value = int(df[column].max())
            else:
                min_value = float(df[column].min())
                max_value = float(df[column].max())
            slider_values[column] = st.sidebar.slider(
                column,
                min_value,
                max_value,
                (min_value, max_value)
            )

        filtered_data = df.copy()
        for column, (min_val, max_val) in slider_values.items():
            filtered_data = filtered_data[
                (filtered_data[column] >= min_val) & (filtered_data[column] <= max_val)
            ]
        return filtered_data

    # Apply filters to the data
    filtered_data = apply_filters(df_train)


    # Exploratory Data Analysis
    if eda_kpi_selection == 'Exploratory Data Analysis (EDA)':
        st.write(
            """This dashboard provides insight into the customer churn data focusing on customer demographics, engagements and other key metrics

        """)

        # Customer Information Analysis
        st. markdown('#### Customer Information Analysis')
        st.write(
            """
        """)
        with st.container():
            col_fig = st.columns([1, 6, 1])
            with col_fig[1]:
                region_plot = px.histogram(df_train, x='REGION', color='CHURN', barmode='group', title='Region Distribution')
                region_plot.update_layout(yaxis_title='Customers')
                st.plotly_chart(region_plot, use_container_width=False)

        # Customer Engagement Analysis
        st.markdown('#### Customer Engagement Analysis')  
        st.write("""
                 
                 """)      
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                top_up_plot = px.histogram(df_train, x='MONTANT', nbins=20, color='CHURN', title='Top-Up Amount Distribution')
                top_up_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(top_up_plot, use_container_width=True)

            with col2:
                recharge_plot = px.histogram(df_train, x='FREQUENCE_RECH', nbins=20, color='CHURN', title='Recharge Frequency Distribution')
                recharge_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(recharge_plot, use_container_width=True)   

        with st.container():
            # Define the correct order of tenure categories
            tenure_order = ['D 3-6 month', 'E 6-9 month', 'F 9-12 month', 'G 12-15 month', 
                'H 15-18 month', 'I 18-21 month', 'J 21-24 month', 'K > 24 month']
            
            col1, col2 = st.columns(2)
            with col1:
                regularity_plot = px.histogram(df_train, x='REGULARITY', nbins=20, color='CHURN', title='Regularity Distribution')
                regularity_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(regularity_plot, use_container_width=True)

            with col2:
                tenure_plot = px.histogram(df_train, x="TENURE", color="CHURN", barmode="group", title="Tenure Distribution", category_orders={"TENURE": tenure_order})
                tenure_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(tenure_plot, use_container_width=True)

        # Correlation and Pair Plot Analysis
        st.markdown("#### Correlation and Pair Plot Analysis")
        st.write(
            "This section investigates the relationships between key numerical features. The correlation heatmap highlights how features correlate with each other, while the pair plot provides a visual exploration of feature interactions."
        )

        with st.container():
            df_train['CHURN'] = df_train['CHURN'].map({'Yes': 1, 'No': 0})
            col1, col2 = st.columns(2)

            with col1:
                # Correlation Heatmap
                corr_features = ["CHURN", "MONTANT", "FREQUENCE_RECH", "REGULARITY", "DATA_VOLUME", "TIGO", "ORANGE", "REVENUE", "ARPU_SEGMENT", "FREQUENCE"]
                corr_matrix = df_train[corr_features].dropna().corr()

                # Annotate the heatmap with correlation values
                heatmap = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale="RdBu",
                    text=corr_matrix.values,  
                    texttemplate="%{text:.2f}",  
                    showscale=True  
                ))

                heatmap.update_layout(
                    title="Correlation Matrix",
                    xaxis_nticks=36
                )

                st.plotly_chart(heatmap)
            
            with col2:
                df_train['CHURN'] = df_train['CHURN'].map({1: 'Yes', 0: 'No'}).fillna('Unknown')
                # Pair Plot
                pairplot_features = ["CHURN", "MONTANT", "REGULARITY", "REVENUE"]
                pairplot_fig = px.scatter_matrix(
                    df_train[pairplot_features],
                    dimensions=["MONTANT", "REGULARITY", "REVENUE"],
                    color="CHURN",
                    title="Pairplot"
                )
                st.plotly_chart(pairplot_fig)

    elif eda_kpi_selection == 'Key Performance Indicators (KPIs)':
        st.write("""
                 
                 """)
        st.markdown("""
        This dashboard provides key performance indicators (KPIs) related to customer churn. It offers insights into:

        - **Total Customers:** Number of customers after applying filters.
        - **Total Customers Retained:** Number of customers retained, showing changes after filtering.
        - **Average Monthly Income:** Changes in the average income of customers.
        - **Total Revenue:** How total revenue of the company has shifted with applied filters.
        - **Churn Rate Gauge:** Visual representation of churn rate changes relative to the unfiltered data.

        Use this dashboard to analyze the impact of various filters on customer retention and overall business metrics.
        """)

        # Apply a map to the data frame for the chun column
        df_train['CHURN'] = df_train['CHURN'].map({'Yes': 1, 'No': 0})
        filtered_data['CHURN'] = filtered_data['CHURN'].map({'Yes': 1, 'No': 0})
  
        # Calculate unfiltered values
        unfiltered_total_customers = df_train.shape[0]
        unfiltered_total_customers_retained = len(df_train[df_train["CHURN"] == 0])
        unfiltered_avg_monthly_income = df_train['REVENUE'].mean()
        unfiltered_total_revenue = df_train['MONTANT'].sum()

        # Churn KPI metrics
        with st.container():
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                # KPI 1: Total Customers
                total_customers = filtered_data.shape[0]
                total_customers_delta = (total_customers - unfiltered_total_customers) / unfiltered_total_customers * 100
                st.metric(
                    label="Total Customers", 
                    value=f"{total_customers:,}", 
                    delta=f"{total_customers_delta:.2f}%", 
                    help="This percentage shows how the total number of customers has changed after applying the selected filters."
                )

            with col2:
                #KPI 2: Total Customers Retained
                total_customers_retained = len(filtered_data[filtered_data["CHURN"] == 0])
                total_customers_retained_delta = (total_customers_retained - unfiltered_total_customers_retained) / unfiltered_total_customers_retained * 100
                st.metric(
                    label="Total Customers Retained", 
                    value=f"{total_customers_retained:,}", 
                    delta=f"{total_customers_retained_delta:.2f}%",
                    help="This percentage shows the change in the number of customers retained after applying the selected filters."
                )

            with col3:
                # KPI 3: Average Monthly Income
                avg_monthly_income = filtered_data['REVENUE'].mean()
                avg_monthly_income_delta = (avg_monthly_income - unfiltered_avg_monthly_income) / unfiltered_avg_monthly_income * 100
                st.metric(
                    label="Avg. Monthly Income", 
                    value=f"CFA {avg_monthly_income:.2f}", 
                    delta=f"{avg_monthly_income_delta:.2f}%",
                    help="This percentage indicates how average monthly income of clients have changed after applying the selected filters."
                )

            with col4:
                # KPI 4: Total Revenue
                total_revenue = filtered_data['MONTANT'].sum()
                total_revenue_delta = (total_revenue - unfiltered_total_revenue) / unfiltered_total_revenue * 100
                st.metric(
                    label="Total Revenue", 
                    value=f"CFA {total_revenue/1e6:,.2f}M", 
                    delta=f"{total_revenue_delta:.2f}%",
                    help="This percentage shows how total revenue has shifted after applying the selected filters."
                )

            # KPI 5: Churn Rate Gauge
        churn_rate = filtered_data['CHURN'].mean() * 100
        unfiltered_churn_rate = df_train['CHURN'].mean() * 100

        fig_churn_rate = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=churn_rate,
            number={'suffix': "%", 'valueformat': ".2f"},
            delta={
                'reference': unfiltered_churn_rate, 
                'relative': True, 
                'position': "top", 
                'valueformat': ".2f",
                'suffix': "%",  
                'increasing': {'color': "red"}, 
                'decreasing': {'color': "green"}  
            },
            title={'text': "Churn Rate"},
            gauge={
                "axis": {"range": [0, 100], "tickformat": ".2f%"},
                "bar": {"color": "blue"},
                "steps": [
                    {"range": [0, 30], "color": "green"},
                    {"range": [30, 70], "color": "yellow"},
                    {"range": [70, 100], "color": "red"}
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": churn_rate
                }
            }
        ))

        st.plotly_chart(fig_churn_rate)
        # Display a description or Chunn Rate Gauge
        st.markdown("""
        **Churn Rate Gauge:** This gauge shows the churn rate based on the filtered dataset, reflecting any adjustments made.

        - **Positive Delta (in red):** Indicates that the churn rate has increased after filtering, meaning more customers are leaving.
        - **Negative Delta (in green):** Indicates that the churn rate has decreased after filtering, meaning fewer customers are leaving.

        In simpler terms, the gauge shows not just the current churn rate but also how the current rate compares to the rate before you applied the filters. 
        For example, if the churn rate was 10% before filtering and now it’s 15%, a positive delta of 50% would show that the churn rate increased by half relative to the initial rate. 
        The gauge provides insights into whether customer retention has improved or worsened after applying your filters.
        """)

        # Insights into Churn by Key Metrics
        st.markdown("#### Insights into Churn by Key Metrics")
        st.markdown("""
        This section explores key factors influencing churn:
        - **Churn Rates by Region:** Examines how churn varies across different regions.
        - **Churn Trends by Customer Tenure:** Illustrates how churn rates change with the length of customer tenure.
        - **Impact of Service Usage on Churn:** Evaluates the relationship between customer churn and their usage patterns, including calls made within the company’s network (ON_NET), calls to competitive providers (ORANGE, TIGO), and data consumption (DATA_VOLUME).
        """)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Plot: Churn Rate by Region
                churn_by_region = filtered_data.groupby('REGION')['CHURN'].mean().reset_index()
                churn_by_region['Churn'] = churn_by_region['CHURN'] * 100
                fig_region_churn = px.bar(churn_by_region, x='REGION', y='CHURN', title='Churn Rate by Region')
                st.plotly_chart(fig_region_churn, use_container_width=True)

            with col2:
                # Plot: Churn Rate Over Tenure
                churn_rate_by_tenure = filtered_data.groupby('TENURE')['CHURN'].mean().reset_index()
                fig_churn_tenure = px.line(churn_rate_by_tenure, x='TENURE', y='CHURN', title='Churn Rate Over Tenure')
                st.plotly_chart(fig_churn_tenure, use_container_width=True)

        # Apply a map to the data frame for the chun column
        filtered_data['CHURN'] = filtered_data['CHURN'].map({1:'Yes', 0:'No'})

        # Define the numerical features and categorize them
        call_data_features = ['ON_NET', 'ORANGE', 'TIGO', 'DATA_VOLUME']

        # Function to categorize features based on quantiles
        def categorize_feature(df, feature):
            low_thresh = df[feature].quantile(0.33)
            high_thresh = df[feature].quantile(0.67)
            
            # Ensure that the thresholds are unique
            if low_thresh == high_thresh:
                high_thresh += 1e-5  # Add a small value to make them unique
            
            df[f'{feature}_category'] = pd.cut(df[feature],
                                            bins=[-np.inf, low_thresh, high_thresh, np.inf],
                                            labels=['Low', 'Medium', 'High'],
                                            duplicates='drop')

        # Assuming df is your DataFrame
        for feature in call_data_features:
            categorize_feature(filtered_data, feature)

        # Create a container and columns for the plots
        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Plot for ON_NET Usage
                on_net_plot = px.histogram(filtered_data, x='ON_NET_category', color='CHURN',
                                            title='ON_NET Usage vs. Churn Status',
                                            color_discrete_map={'Yes': 'red', 'No': 'green'})
                on_net_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(on_net_plot, use_container_width=True)

            with col2:
                # Plot for ORANGE Usage
                orange_plot = px.histogram(filtered_data, x='ORANGE_category', color='CHURN',
                                            title='ORANGE Usage vs. Churn Status',
                                            color_discrete_map={'Yes': 'red', 'No': 'green'})
                orange_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(orange_plot, use_container_width=True)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Plot for TIGO Usage
                tigo_plot = px.histogram(filtered_data, x='TIGO_category', color='CHURN',
                                            title='TIGO Usage vs. Churn Status',
                                            color_discrete_map={'Yes': 'red', 'No': 'green'})
                tigo_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(tigo_plot, use_container_width=True)

            with col2:
                # Plot for DATA_VOLUME Usage
                data_volume_plot = px.histogram(filtered_data, x='DATA_VOLUME_category', color='CHURN',
                                                title='DATA_VOLUME Usage vs. Churn Status',
                                                color_discrete_map={'Yes': 'red', 'No': 'green'})
                data_volume_plot.update_layout(yaxis_title="Customers")
                st.plotly_chart(data_volume_plot, use_container_width=True) 

        # Company Revenue and Customer Income Insights
        st.markdown("#### Company Revenue and Customer Income Insights")
        st.markdown("""
        This section provides detailed insights into company revenue and customer income patterns:
        - **Average Monthly Income by Region:** Shows the average income that customers generate per month across different regions.
        - **Average Revenue by Region:** Displays the average revenue earned by the company from customers in each region.
        - **Average Monthly Income by Tenure:** Illustrates how the average monthly income of customers changes with their length of tenure.
        - **Average Revenue by Tenure:** Highlights the average revenue the company earns from customers based on their tenure.
        """)


        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Plot: Average Monthly Income by Region
                avg_income_by_region = filtered_data.groupby('REGION')['REVENUE'].mean().reset_index()
                fig_avg_income_by_region = px.bar(avg_income_by_region, x='REGION', y='REVENUE', title='Avg. Monthly Income by Region')
                st.plotly_chart(fig_avg_income_by_region)

            with col2:
                # Plot: Average Revenue by Region
                total_revenue_by_region = filtered_data.groupby('REGION')['MONTANT'].mean().reset_index()
                fig_total_revenue_by_region = px.bar(total_revenue_by_region, x='REGION', y='MONTANT', title='Avg. Revenue by Region')
                st.plotly_chart(fig_total_revenue_by_region)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Plot: Average Monthly Income by Tenure
                avg_income_by_tenure = filtered_data.groupby('TENURE')['REVENUE'].mean().reset_index()
                fig_avg_income_by_tenure = px.bar(avg_income_by_tenure, x='TENURE', y='REVENUE', title='Avg. Monthly Income by Tenure')
                st.plotly_chart(fig_avg_income_by_tenure)

            with col2:
                # Plot: Average Revenue by Tenure
                total_revenue_by_tenure = filtered_data.groupby('TENURE')['MONTANT'].mean().reset_index()
                fig_total_revenue_by_tenure = px.bar(total_revenue_by_tenure, x='TENURE', y='MONTANT', title='Avg. Revenue by Tenure')
                st.plotly_chart(fig_total_revenue_by_tenure)

        # KPI data
        kpi_data = {
            'KPI': ['Total Customers', 'Total Customers Retained', 'Churn Rate', 'Avg. Monthly Income', 'Total Revenue'],
            'Value': [f"{total_customers:,}", f"{total_customers_retained:,}", f"{churn_rate:.2f}%", f"CFA {avg_monthly_income:.2f}", f"CFA {total_revenue:,.2f}"]
        }

        # Create DataFrame
        kpi_df = pd.DataFrame(kpi_data)
        kpi_df.set_index('KPI', inplace=True)

        # Function to apply conditional formatting based on the value
        def color_kpi_value(value):
            if '%' in value:
                percent_value = float(value.strip('%'))
                if percent_value < 30:
                    color = 'green'
                elif 30 <= percent_value < 70:
                    color = 'yellow'
                else:  
                    color = 'red'
            else:
                color = 'lightblue'
            return f'color: {color}'

        # Function to apply conditional formatting
        def highlight_churn(index):
            color = 'background-color: #4B61F5' if index.name == 'Total Revenue' else ''
            return [color] * len(index)

        # Apply the color_negative_red function to the 'Value' column
        styled_df = kpi_df.style.applymap(color_kpi_value, subset=['Value'])

        # Apply the highlight_churn function to the entire row
        styled_df = styled_df.apply(highlight_churn, axis=1)

        # Display the styled DataFrame
        st.markdown("#### Key Performance Indicators (KPIs)")
        st.table(styled_df)
               