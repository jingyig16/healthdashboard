import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from data import valid_variables
from data import read_data

data = read_data()

# Create the dropdown menu to select a time period
def create_time_period_dropdown():
    """ Creates a dropdown with 4 values: Daily, Hourly,
        Minute-by-Minute, and Second-by-Second.

    :return: Drop down to select time period for time series visualization
    """
    return dcc.Dropdown(
        id='time-period-dropdown',
        options=[{'label': 'Daily', 'value': 'D'},
                 {'label': 'Hourly', 'value': 'H'},
                 {'label': 'Minute-by-Minute', 'value': 'M'},
                 {'label': 'Second-by-Second', 'value': 'S'}],
        value='D'
    )


# Create the dropdown menu to select a variable
category_dropdown_menu = dcc.Dropdown(
    id='variable-dropdown1',
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
    # Get the valid variables for the specified time period
    valid_vars = valid_variables.get(time_period)

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
    elif time_period == 'S':
        user_data['ActivitySecond'] = pd.to_datetime(user_data['ActivitySecond'], format='%m/%d/%Y %I:%M:%S %p')

    # Create the visualization using Plotly Express
    if time_period == 'D':
        fig = px.line(user_data, x='ActivityDay', y=variable, title=variable)
    elif time_period == 'H':
        fig = px.line(user_data, x='ActivityHour', y=variable, title=variable)
    elif time_period == 'M':
        fig = px.line(user_data, x='ActivityMinute', y=variable, title=variable)
    elif time_period == 'S':
        fig = px.line(user_data, x='ActivitySecond', y=variable, title=variable)

    return fig

def time_series_page():
    """ Defines the layout for the time series page in the dashboard
        with headings, multiple rows and columns, and graphs.

    :return: The layout for the time series page in the dashboard
    """
    return dbc.Container([
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div([
                    html.H5("Filters"),
                    html.Hr(),
                    html.Label("Select Time Period:"),
                    create_time_period_dropdown(),
                    html.Br(),
                    html.Label("Select a Visualization:"),
                    category_dropdown_menu,
                    html.Br(),
                    html.Label("Enter Your User ID:"),
                    dcc.Dropdown(id='user-id', options=[], placeholder='Enter User ID', searchable=True),
                ], className="bg-light sidebar", style={'border': '3px solid #000', 'height': '100%'})
            ], md=3, className="text-center"),

            # Main content
            dbc.Col([
                html.H1("Time Series Visuals", className="text-center"),
                dcc.Graph(id='time-series-chart')
            ], md=9, className="main-content")
        ], style={'margin-right': '0', 'margin-left': '0'})
    ], fluid=True)


