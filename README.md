
# **Customer Churn Capstone Project**

**A powerful machine learning-based application to predict customer churn for telco companies.**

## Introduction
This app is designed to predict customer churn for telecomunications companies in the business of providing customers with airtime and mobile data bundles

## App Features

### Key Features
- Real-time data analysis
- Advanced machine learning algorithms for predicting customer churn
- Customizable dashboards and reports

## Demo
### Watch Demo Video
[Watch the demo video](https://www.youtube.com/watch?v=8lGpZkjnkt4) to see the Customer Churn Predictor App in action and learn how to maximize its potential.

## Installation

### How to Run the Application
To run the Customer Churn App locally, follow these steps:


1. Clone the repository:
   ```bash
   git clone https://github.com/worlakuma/Customer_Churn_Cap.git
   cd Customer_Churn
   ```
2. Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run Homepage.py
   ```

For a smooth setup, ensure all dependencies are correctly installed.

## Usage
Once installed, the app can be accessed via your web browser at `http://localhost:8501`. The homepage provides an overview of the app and the the team of developers behind its production. A history page is available to provide an overview of your current data and churn predictions.


## Machine Learning Integration
The Churn Predictor App uses powerful machine learning models like Random Forest, K-Nrearest Neighbors, and Feedforward Neural Network to predict churn. The models have been fine-tuned for accuracy, and the app provides probability estimates for each prediction, allowing businesses to prioritize retention efforts.

## App Structure
The app is organized into several key sections:

1. **Homepage**: 
   - This section contains pages focused on user engagement and access, including the home page, about us and login functionality. It serves as the gateway for users to interact with the platform. Details of the app features are included here as well.

2. **Dashboard**:
   - This section houses tools for managing and analyzing data. It includes pages that provide an overview of the data and visualizations through an analytics dashboard. It’s where users can access and manipulate the core data.

3. **Data**:
   - This page is desinged to provide users with a comprehensive and interactive interface for accessing and managing data

4. **History**:
   - This section provides users with information on all previous and current single predictions

5. **Predictions**:
   - This section is dedicated to generating insights from historical data and predicting future trends. It includes pages focused on exploring historical data and making projections based on that data.


## Contact Information
### Need Help?
For support, collaboration, or any inquiries, please contact us at:
- **Email**: [sdi@azubiafrica.com](mailto:wolakuma@gmail.com)
- **LinkedIn**: [Link](https://www.linkedin.com/in/gabrielkuma/)


### Colaborators

**Nfayem Imoro** 

**Jackline Wangari Maina** 

**Obed Korda** 

**Godfred Frank Aning**

**Victor Obondo**


## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/worlakuma/Customer_Churn_Cap/blob/main/LICENSE) file for details.

## Development Workflow:

1. **Local Development**:
   - Develop and test machine learning models locally.
   - Develop and test Streamlit app by intergrating the trained models locally.
   - Ensure that all features work as expected.
   - Fix any bugs or issues that arise during development.

2. **Containerization**:
   - Create a `Dockerfile` to define app’s environment and dependencies.
   - Build the Docker image and test it locally to ensure that it works in the containerized environment.
   - Use Docker Compose if needed to manage complex setups with multiple services.

3. **Deployment**:
   - Push the Docker image to a container registry (e.g., Docker Hub).
   - Deploy the containerized app to a production environment or cloud service.

4. **Testing**:
   - Test the containerized app in staging or a test environment to ensure it behaves as expected before production deployment.

---
