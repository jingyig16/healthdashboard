"""
Anoushka Bhatia, Xi Chen, Jai Gollapudi, Jingyi Gong, Krishi Patel, Shreya Thalvayapati
DS3500 Final Project: Fitbit Insights Dashboard
4/19/2023
time_series.py: individual file for Time Series Visuals
Github repo: https://github.com/jingyig16/healthdashboard
"""

# Importing libraries
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html


# Create the dropdown menu to select a time period
def create_time_period_dropdown1():
    """ Creates a dropdown with 4 values: Daily, Hourly,
        Minute-by-Minute, and Second-by-Second.

    :return: Drop down to select time period for time series visualization
    """
    return dcc.Dropdown(
        id='time-period-dropdown1',
        options=[{'label': 'Daily', 'value': 'D'},
                 {'label': 'Hourly', 'value': 'H'},
                 {'label': 'Minute-by-Minute', 'value': 'M'},
                 {'label': 'Second-by-Second', 'value': 'S'}],
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
    """ Extracts data based on variable, time period, and user ID;
        Converts to datetime format; Creates visualization.

    :param variable: The variable the user wants to explore
    :param time_period: The time period the user chooses
    :param user_id: The user's ID number
    :param data: The DataFrame
    :return: Plotly linegraph figure
    """

    # Extract the relevant data from the data dictionary
    data_df = data[time_period][variable]
    user_data = data_df[data_df['Id'] == user_id]

    # Convert the time variable to datetime format
    if time_period == 'D':
        user_data['ActivityDay'] = pd.to_datetime(user_data['ActivityDay'])
        fig = px.line(user_data, x='ActivityDay', y=variable,
                      title=f'Line plot of Daily {variable}')
    elif time_period == 'H':
        user_data['ActivityHour'] = pd.to_datetime(user_data['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
        fig = px.line(user_data, x='ActivityHour', y=variable,
                      title=f'Line plot of Hourly {variable}')
    elif time_period == 'M':
        user_data['ActivityMinute'] = pd.to_datetime(user_data['ActivityMinute'], format='%m/%d/%Y %I:%M:%S %p')
        fig = px.line(user_data, x='ActivityMinute', y=variable,
                      title=f'Line plot of Minute-by-Minute {variable}')
    elif time_period == 'S':
        user_data['ActivitySecond'] = pd.to_datetime(user_data['ActivitySecond'], format='%m/%d/%Y %I:%M:%S %p')
        fig = px.line(user_data, x='ActivitySecond', y=variable,
                      title=f'Line plot of Second-by-Second {variable}')

    return fig


def time_series_page():
    """ Defines the layout for the time series page in the dashboard
        with headings, multiple rows and columns, and graphs.

    :return: The layout for the time series page in the dashboard
    """
    return dbc.Container([
        html.Br(),
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div([
                    html.H5("Filters"),
                    html.Hr(),
                    html.Label("Select Time Period:"),
                    create_time_period_dropdown1(),
                    html.Br(),
                    html.Label("Select a variable:"),
                    category_dropdown_menu,
                    html.Br(),
                    html.Label("Enter Your User ID:"),
                    dcc.Dropdown(id='user-id-ts', options=[], placeholder='Enter User ID', searchable=True),
                ], className="bg-light sidebar", style={
                    'border': '1px solid white',
                    'borderRadius': '15px',
                    'height': '80%',
                    'padding': '20px',
                    'margin-top': '100px',
                })
            ], md=3, className="text-center"),

            # Main content
            dbc.Col([
                html.Br(),
                html.H1("Time Series Visuals", className="text-center", style={'color': 'white'}),
                dcc.Graph(id='time-series-chart')
            ], md=9, className="main-content", style={
                'padding': '20px',
                'backgroundColor': 'black',
                'borderRadius': '15px',
                'height': '80%',
            })
        ], style={'margin-right': '0', 'margin-left': '0', 'backgroundColor': 'black'}, className="align-items-start")
    ], fluid=True)


