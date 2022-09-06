# Firstly import the packages

import pysd
from IPython.display import Image
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
model = pysd.read_xmile('Stella_Model/smoking cessation demo.stmx')

# Name the app

st.title('Smoking Cessation SD Model Demo')

# Add Variables to the Smoking Cessation SD Class object

st.subheader('Slide the Slider to Vary Smoking Cessation Re-Investment Levels')
re_investment = st.slider("Proportion of Savings Spent on Cessation", 1, 100, 1)

# Run the Model
values = model.run(params={'Percentage of savings spent on cessation': re_investment})

# Export the Simulation Results

df_smoking = values[['Current smokers', 'Ex smokers', 'Lapsed ex smokers']]

st.subheader('Effects of Re-Investment on Smoking Levels')
st.line_chart(df_smoking)