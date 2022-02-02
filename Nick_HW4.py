# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 10:09:43 2022

@author: nicholas.assad
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

st.title("Data Exploration of Craft Beers in the United States")

url = r"https://github.com/nickassad39/Nick-App/blob/main/beers.csv"

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
    with open('pipe.pkl', 'rb') as pickled_mod_HW:
        model = pickle.load(pickled_mod_HW)
    return model

df = load_data(num_rows)

if section == 'Data Explorer':
    
    
    x_axis = st.sidebar.selectbox("Choose column for X-axis", 
                                  df.select_dtypes(include = np.object).columns.tolist())
    
    y_axis = st.sidebar.selectbox("Choose column for y-axis", ['ibu', 
                                                               'abv'])
    
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
    
    ounces = st.sidebar.radio("Choose Ounces", 
                                  df['ounces'].unique().tolist())
    state = st.sidebar.selectbox("What State is the beer brewed in?",
                                  df['state'].unique().tolist())
    city = st.sidebar.selectbox("City", 
                                  df['city'].unique().tolist())    
    style = st.sidebar.selectbox("What style is the beer?", 
                                  df['style'].unique().tolist())
    brewery = st.sidebar.radio("What brewery was t?",
                                  df['brew_name'].unique().tolist())
 
    sample = {
    'ounces': ounces,
    'state': state,
    'city': city,
    'style': style,
    'brew_name': brewery,
    }

    sample = pd.DataFrame(sample, index = [0])
    prediction = model.predict(sample)[0]
    
    st.title(f"Predicted ABV of Craft Beers: {int(prediction)}")