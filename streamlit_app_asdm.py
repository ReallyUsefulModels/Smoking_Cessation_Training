import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from ASDM.ASDM import Structure

def load_model(model_path):
    try:
        model = Structure(from_xmile=model_path)
    except FileNotFoundError:
        st.error(f"File {model_path} not found.")
        return None
    return model

def run_simulation(model, simulation_time, re_investment):
    model.sim_specs['initial_time'] = 0
    model.sim_specs['current_time'] = 0
    model.sim_specs['dt'] = 1
    model.sim_specs['simulation_time'] = simulation_time
    model.sim_specs['time_units'] = 'Months'

    model.clear_last_run()

    model.replace_element_equation('Percentage_of_savings_spent_on_cessation', re_investment)

    model.simulate()

    results = model.export_simulation_result()
    results_df = pd.DataFrame.from_dict(results)

    columns_to_plot = ["Current_smokers", "Ex_smokers", "Ex_smokers_starting_again"]
    return results_df['Months'], results_df[columns_to_plot]

st.title('Smoking Cessation')

st.markdown("""
This simulation estimates the effects of various reinvestment levels in a smoking cessation service within a population of 900 smokers. 
By varying the proportion of savings that are reinvested into the service, we can observe different outcomes in terms of current smokers, ex-smokers, 
and ex-smokers who start smoking again over time.
""")
            
st.subheader('Slide the Slider to Vary Re-Investment Levels')

model = load_model('models/smoking cessation demo.stmx')

if model is not None:
    re_investment = st.slider("Proportion of Savings Spent on Cessation", 0, 100, 45)
    simulation_time = st.slider("Select the number of months to simulate:", min_value=1, max_value=36, value=24)

    x_values, y_values = run_simulation(model, simulation_time, re_investment)

    st.subheader('Effects of Re-Investment on Smoking Levels')

    fig = go.Figure()
    for column in y_values.columns:
        fig.add_trace(go.Scatter(x=x_values, y=y_values[column], mode='lines', name=column))
    fig.update_layout(xaxis_title='Months', yaxis_title='Number of Smokers', autosize=False, width=800, height=500)
    st.plotly_chart(fig)