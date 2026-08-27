# APEX-Agentic-Smart-Agriculture-Advisory
# 🌱 Crop Recommendation System

A Machine Learning-based Crop Recommendation System that recommends the most suitable crop based on soil and environmental conditions.

The model takes the following parameters as input:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

A Random Forest classification model is trained on these agricultural parameters to predict the most suitable crop. The trained model is integrated into a Streamlit web application, where users can enter field conditions and receive a crop recommendation along with the prediction confidence and top 3 recommended crops.

## 🛠️ Tech Stack

- Python
- Pandas
- Scikit-learn
- Random Forest
- Joblib
- Streamlit

## 🚀 Features

- Crop recommendation based on soil and environmental conditions
- Machine Learning-based prediction
- Prediction confidence score
- Top 3 crop recommendations
- Interactive Streamlit web application
