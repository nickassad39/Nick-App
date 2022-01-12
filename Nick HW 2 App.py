# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 20:21:15 2022

@author: nicholas.assad
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

st.title("Data Exploration of American Health Insurance Policies")

url = r"C:\Users\nicholas.assad\dat-11-15\Homework\Unit2\data\insurance_premiums.csv"

num_rows = st.sidebar.number_input('Select Number of Rows to Load', 
                                   min_value = 50, 
                                   max_value = 1400, 
                                   step = 50)

section = st.sidebar.radio('Choose Application Section', ['Data Explorer','Model Explorer'])
print(section)

@st.cache
def load_data(num_rows):
    df = pd.read_csv(url, nrows = num_rows)
    return df

@st.cache
def create_grouping(x_axis, y_axis):
    grouping = df.groupby(x_axis)[y_axis].mean()
    return grouping

def load_model():
    with open('pipe.pkl', 'rb') as pickled_mod:
        model = pickle.load(pickled_mod)
    return model

df = load_data(num_rows)

if section == 'Data Explorer':
    
    
    x_axis = st.sidebar.selectbox("Choose column for X-axis", 
                                  df.select_dtypes(include = np.object).columns.tolist())
    
    y_axis = st.sidebar.selectbox("Choose column for y-axis", ['charges', 
                                                               'bmi'])
    
    chart_type = st.sidebar.selectbox("Choose Your Chart Type", 
                                      ['line', 'bar', 'area'])
    
    if chart_type == 'line':
        grouping = create_grouping(x_axis, y_axis)
        st.line_chart(grouping)
        
    elif chart_type == 'bar':
        grouping = create_grouping(x_axis, y_axis)
        st.bar_chart(grouping)
    elif chart_type == 'area':
        fig = px.strip(df[[x_axis, y_axis]], x=x_axis, y=y_axis)
        st.plotly_chart(fig)
    
    st.write(df)
    
else:
    st.text("Choose Options to the Side to Explore the Model")
    model = load_model()
    
    gender = st.sidebar.selectbox("Choose Sex", 
                                  df['sex'].unique().tolist())
    age = st.sidebar.selectbox("What is the Insured's Age",
                                  df['age'].unique().tolist())
    region = st.sidebar.selectbox("Region", 
                                  df['region'].unique().tolist())
    children = st.sidebar.selectbox("How Many Kids Does the Insured Have?", 
                                  df['children'].unique().tolist())
    
    sample = {
    'sex': gender,
    'age': age,
    'region': region,
    'children': children
    }

    sample = pd.DataFrame(sample, index = [0])
    prediction = model.predict(sample)[0]
    
    st.title(f"Predicted Attendance: {int(prediction)}")


