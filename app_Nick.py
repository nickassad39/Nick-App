# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 18:51:04 2022

@author: nicholas.assad
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title("My First Dashboard")

url = r"https://raw.githubusercontent.com/JonathanBechtel/dat-11-15/main/ClassMaterial/Unit1/data/master.csv"

num_rows = st.sidebar.number_input('Select Number of Rows to Load', 
                                   min_value=1000,
                                   max_value=50000,
                                   step=1000)

section = st.sidebar.radio('Choose Application Section', ['Data Explorer','Model Explorer'])
print(section)

@st.cache
def load_data(num_rows):
    df = pd.read_csv(url, parse_dates=['visit_date'], nrows=num_rows)
    return df

def load_model():
    with open ('pipe.pkl','rb') as pickled_mod:
        model = pickle.load(pickled_mod)
    return model

@st.cache
def create_grouping(x_axis, y_axis):
    grouping = df.groupby(x_axis)[y_axis].mean()
    return grouping

if section == 'Data Explorer':
    
    df = load_data(num_rows)

    x_axis = st.sidebar.selectbox("Choose Column for X-axis",
                                  df.select_dtypes(include = np.object).columns.tolist())
    
    y_axis = st.sidebar.selectbox("Choose Column for Y-axis",
                                  ['visitors','reserve_visitors'])
    
    grouping = df.groupby(x_axis)[y_axis].mean()
    
    chart_type = st.sidebar.selectbox("Choose Your Chart Type",
                                      ['line','bar'])

    if chart_type =='line':
        grouping = create_grouping(x_axis, y_axis)
        st.line_chart(grouping)
   
    elif chart_type == 'bar':
        grouping = create_grouping(x_axis, y_axis)
        st.bar_chart(grouping)    
    
    st.write(df)
   
else:
    st.text("Choose Options to the Side to Explore the Model")
    model = load_model()
    
    id_val = st.sidebar.selectbox("Choose Restaurant ID",
                                  df['id'].unique().tolist())
    yesterday = st.sidebar.number_input("How many visitors yesterday", min=0,
                                         max=100, step=1, value=20)
    day_of_week = st.sidebar.selectbox("Day of Week",
                                   df['day_of_week'].unique().tolist())                           

    sample = {
        'id': id_val
        'yesterday': yesterday
        'day_of_week': day_of_week
        }
    
    sample = pd.DataFrame(sample, index=[0])
    prediction = model.predict(sample)[0]
    
    st.title(f"Predicted Attendance: {int(prediction)}")