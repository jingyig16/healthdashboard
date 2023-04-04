import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from data import valid_variables


# Create the dropdown menu to select a time period
def create_time_period_dropdown():
    return dcc.Dropdown(
        id='time-period-dropdown',
        options=[{'label': 'Daily', 'value': 'D'},
                 {'label': 'Hourly', 'value': 'H'},
                 {'label': 'Minute-by-Minute', 'value': 'M'}],
        value='D'
    )


# Create the dropdown menu to select a variable
category_dropdown_menu = dcc.Dropdown(
    id='variable-dropdown',
    options=[],
    value=None
)

# Create the time series chart
def create_time_series(variable, time_period, user_id, data):
    # Get the valid variables for the specified time period
    valid_vars = valid_variables.get(time_period)

    # Check if the specified variable is valid for the specified time period
    # if variable not in valid_vars:
    #    raise ValueError(f"{variable} is not a valid variable for time period {time_period}")

    # Extract the relevant data from the data dictionary
    data_df = data[time_period][variable]
    user_data = data_df[data_df['Id']==user_id]

    # Convert the time variable to datetime format
    if time_period == 'D':
        user_data['ActivityDay'] = pd.to_datetime(user_data['ActivityDay'])
    elif time_period == 'H':
        user_data['ActivityHour'] = pd.to_datetime(user_data['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
    elif time_period == 'M':
        user_data['ActivityMinute'] = pd.to_datetime(user_data['ActivityMinute'], format='%m/%d/%Y %I:%M:%S %p')

    # Create the visualization using Plotly Express
    if time_period == 'D':
        fig = px.line(user_data, x='ActivityDay', y=variable, title=variable)
    elif time_period == 'H':
        fig = px.line(user_data, x='ActivityHour', y=variable, title=variable)
    elif time_period == 'M':
        fig = px.line(user_data, x='ActivityMinute', y=variable, title=variable)

    return fig

def time_series_page():
    return dbc.Container([
        html.H1("Time Series Visuals", className="text-center"),
        dbc.Row([
            dbc.Col([
                html.Label("Select Time Period:"),
                create_time_period_dropdown()
            ], md=4),
            dbc.Col([
                html.Label("Select a Visualization:"),
                category_dropdown_menu,
            ], md=4),
            dbc.Col([
                html.Label("Enter Your User ID:"),
                dcc.Input(id='user-id', type='number', placeholder='Enter User ID'),
            ], md=4)
        ], className='my-3'),
        dcc.Graph(id='time-series-chart')
    ])


