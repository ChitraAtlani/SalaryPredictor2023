from cmath import e
from datetime import time
import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]

# Create a mapping for country and education
country_mapping = {
    "United States of America": 0,
    "Germany": 1,                                              
"United Kingdom of Great Britain and Northern Ireland" : 2,   
"India" : 3,                                               
"Canada" : 4,                                                 
"France" :5,                                                
"Brazil " :6,                                               
"Spain "  :7 ,                                             
"Netherlands" :8,                                           
"Australia" :9 ,                                         
"Italy":10,                                        
"Poland" :11,                                       
"Sweden" :12,                                     
"Russian Federation":13,                                  
"Switzerland":14                                              
}

education_mapping = {
    "Bachelors degree": 0,
    "Masters degree": 1,
    "Less than a Bachelors":2,
    "Post grad":3       
}

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")

    countries = tuple(country_mapping.keys())
    education = tuple(education_mapping.keys())

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate salary")
    if ok:
        # Convert the selected country and education to numerical values
        country_encoded = country_mapping[country]
        education_encoded = education_mapping[education]

        x = np.array([[country_encoded, education_encoded, experience]], dtype=float)

        salary = regressor.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

