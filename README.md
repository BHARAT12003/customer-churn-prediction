# Customer Churn Prediction and Retention Analysis Using Machine Learning

A machine learning web application that predicts whether a customer is likely to churn and provides a churn probability, risk level, risk factors, and personalized retention recommendations.

## Project Overview

Customer churn is an important challenge for subscription-based businesses. This project uses machine learning to analyze customer information and predict the likelihood of customer churn.

The application combines a machine learning backend with an interactive web frontend to provide an easy-to-understand churn prediction and retention analysis.

## Key Features

- Customer churn prediction using Machine Learning
- Churn probability calculation
- Low, Medium, and High risk classification
- Risk score visualization
- Identification of important customer risk factors
- Personalized retention recommendations
- Comparison of multiple machine learning models
- Interactive web-based interface
- REST API using Flask
- Exploratory Data Analysis with visualizations

## Machine Learning Models

The following models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Logistic Regression was selected as the final model based on its F1 Score among the evaluated models.

## Dataset

The project uses the Telco Customer Churn dataset.

The dataset contains customer information such as:

- Customer tenure
- Contract type
- Internet service
- Monthly charges
- Total charges
- Payment method
- Online security
- Technical support
- Churn status

## Project Workflow

Customer Data
        ↓
Data Preprocessing
        ↓
Exploratory Data Analysis
        ↓
Train Multiple ML Models
        ↓
Evaluate Models
        ↓
Select Final Model
        ↓
Flask Prediction API
        ↓
Interactive Frontend
        ↓
Churn Prediction + Risk Analysis
        ↓
Retention Recommendations

## Technologies Used

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib

### Backend
- Flask
- Flask-CORS

### Frontend
- HTML
- CSS
- JavaScript

### Data Visualization
- Matplotlib
- Seaborn

## Project Structure

```text
customer-churn-prediction/
│
├── backend/
│   ├── app.py
│   ├── preprocess_data.py
│   ├── eda_analysis.py
│   └── train_models.py
│
├── dataset/
│   ├── customer_churn.csv
│   └── processed_churn.csv
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── model/
│   ├── churn_model.pkl
│   ├── scaler.pkl
│   └── feature_columns.pkl
│
├── results/
│   ├── churn_distribution.png
│   ├── churn_vs_tenure.png
│   ├── churn_vs_monthly_charges.png
│   ├── churn_by_contract.png
│   └── churn_by_internet_service.png
│
├── notebooks/
├── requirements.txt
└── README.md