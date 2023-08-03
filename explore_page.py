import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

def shorten_categories(categories, cutoff): #categories are value counts & cutoff where we adjust ormake cutoffs whatever we want
        categorical_map = {}
        for i in range (len(categories)):
            if categories.values[i] >= cutoff:
                categorical_map[categories.index[i]] = categories.index[i]
            else:
                categorical_map[categories.index[i]]= 'Other'
        return categorical_map
    
def clean_experience(x):
    if pd.isna(x) or x == '':
        return np.nan
    if x == 'More Than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    if ',' in x:
        x = x.replace(',', '')  # Remove commas from the string
    try:
        return float(x)
    except ValueError:
        return np.nan
    
def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelors degree'
    if 'Master’s degree' in x:
        return 'Masters degree'
    if 'Professional degree' in x or 'Other Doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'
 
st.cache_data  # used as fuction which does the overide where the function is conducted in loop so to eliminate those conditions to maintain the loop i.e override
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCodePro","Employment","ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment" , axis=1)
    
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df=df[df["ConvertedCompYearly"] <= 200000 ]
    df = df[df["ConvertedCompYearly"] >= 100000]
    df= df[df["Country"] != "Other"]
    
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df ["EdLevel"] = df["EdLevel"].apply(clean_education)    
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis=1)
    return df

df= load_data()

def show_explore_page():
    st.title("Explore software Engineer Salaries")
    st.write(
        """### Stack Overflow Developer Survey 2023"""
    )

    data= df["Country"].value_counts()
    
    
# Create a pie chart with equal spacing and labels inside the chart
    fig1, ax1 = plt.subplots(figsize=(8, 8))  # Adjust the figure size to allow more space for labels
    fig1, ax1 = plt.subplots()
    # ax1.pie(data, shadow=True, startangle=90, pctdistance=0.9)
    _, texts, autotexts = ax1.pie(data, labels=data.index, autopct="%0.1f%%", shadow=True, startangle=90, labeldistance=1 )
    ax1.axis("equal")  #Equal aspect ratio ensures that pie is drawn as circle.    
    ax1.set_facecolor('lightgray')
    for text, autotext in zip(texts, autotexts):
        text.set(color="black", fontsize=10)
    text.set_horizontalalignment('center')
    text.set_verticalalignment('center')
    text.set(fontsize=13,color="black", fontweight="bold")
    autotext.set(color="white", fontsize=13 , fontweight="bold")
    
    ax1.set_title("Country Distribution")
    ax1.legend(data.index, title="Countries", loc="center left", bbox_to_anchor=(1, -0.05, 0.5, 0))
        
        
    st.write("""### Number of Data from different countries""") 
    st.pyplot(fig1)
    
    st.write("""### Mean Salary Based On Country""")
    data= df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    data= df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)