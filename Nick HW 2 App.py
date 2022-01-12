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




