import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.graph_objects as go
from data import read_data
from scipy.stats import linregress

data = read_data()
# Create the dropdown menu to select a time period
def create_time_period_dropdown2():
    """ Creates a dropdown with 4 values: Daily, Hourly,
        Minute-by-Minute, and Second-by-Second.

    :return: Drop down to select time period for correlation visualization
    """
    return dcc.Dropdown(
        id='time-period-dropdown2',
        options=[{'label': 'Daily', 'value': 'D'},
                 {'label': 'Hourly', 'value': 'H'},
                 {'label': 'Minute-by-Minute', 'value': 'M'},
                 {'label': 'Second-by-Second', 'value': 'S'}],
        value='D'
    )


# Create the dropdown menu to select a variable
variable_dropdown_menu1 = dcc.Dropdown(
    id='variable-dropdown1',
    options=[],
    value=None
)

# Create the dropdown menu to select a variable
variable_dropdown_menu2 = dcc.Dropdown(
    id='variable-dropdown2',
    options=[],
    value=None
)




def create_corr(variable1, variable2, time_period,  user_id, data):
    """ Extracts data based on variables, time period, and user ID;
        Converts to datetime format; Creates visualization.

    :param variable1: The first variable the user wants to explore
    :param variable2: The second variable the user wants to explore
    :param time_period: The time period the user chooses
    :param user_id: The user's ID number
    :param data: The DataFrame
    :return: Plotly scatter plot figure with line of best fit
    """

    # Extract the relevant data from the data dictionary
    data_df1 = data[time_period][variable1]
    data_df2 = data[time_period][variable2]
    user_data1 = data_df1[data_df1['Id'] == user_id]
    user_data2 = data_df2[data_df2['Id'] == user_id]

    # Convert the time variable to datetime format
    if time_period == 'D':
        user_data1['ActivityDay'] = pd.to_datetime(user_data1['ActivityDay'])
        user_data2['ActivityDay'] = pd.to_datetime(user_data2['ActivityDay'])
    elif time_period == 'H':
        user_data1['ActivityHour'] = pd.to_datetime(user_data1['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
        user_data2['ActivityHour'] = pd.to_datetime(user_data2['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
    elif time_period == 'M':
        user_data1['ActivityMinute'] = pd.to_datetime(user_data1['ActivityMinute'], format='%m/%d/%Y %I:%M:%S %p')
        user_data2['ActivityMinute'] = pd.to_datetime(user_data2['ActivityMinute'], format='%m/%d/%Y %I:%M:%S %p')
    elif time_period == 'S':
        user_data1['ActivitySecond'] = pd.to_datetime(user_data1['ActivitySecond'], format='%m/%d/%Y %I:%M:%S %p')
        user_data2['ActivitySecond'] = pd.to_datetime(user_data2['ActivitySecond'], format='%m/%d/%Y %I:%M:%S %p')

    # Calculate the line of best fit
    slope, intercept, r_value, _, _ = linregress(user_data1[variable1], user_data2[variable2])
    best_fit_x = np.linspace(user_data1[variable1].min(), user_data1[variable1].max(), 2)
    best_fit_y = slope * best_fit_x + intercept

    # Create an empty figure
    fig = go.Figure()

    # Add scatter plot for variable1 and variable2
    fig.add_trace(go.Scatter(x=user_data1[variable1], y=user_data2[variable2], mode='markers',
                             name=f'{variable1} vs {variable2} (r = {r_value:.2f})',
                             marker=dict(color="blue", opacity=0.7)))

    # Add the line of best fit
    fig.add_trace(go.Scatter(x=best_fit_x, y=best_fit_y, mode='lines', name='Line of Best Fit',
                             line=dict(color='red', width=2)))

    # Update the layout
    fig.update_layout(title=f"{variable1} vs {variable2}",
                      xaxis_title=variable1,
                      yaxis_title=variable2)

    # Display the figure
    return fig
    

def correlation_page():
    """ Defines the layout for the correlation page in the dashboard
        with headings, multiple rows and columns, and graphs.

    :return: The layout for the correlation page in the dashboard
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
                    create_time_period_dropdown2(),
                    html.Br(),
                    html.Label("Select a variable:"),
                    variable_dropdown_menu1,
                    html.Br(),
                    html.Label('Select a variable:'),
                    variable_dropdown_menu2,
                    html.Br(),
                    html.Label("Enter Your User ID:"),
                    dcc.Dropdown(id='user-id-corr', options=[], placeholder='Enter User ID', searchable=True),
                ], className="bg-light sidebar", style={
                    'border': '1px solid white',
                    'borderRadius': '15px',
                    'height': '80%',
                    'padding': '20px',
                })
            ], md=3, className="text-center"),

            # Main content
            dbc.Col([
                html.Br(),
                html.H1("Correlation Exploration", className="text-center", style={'color': 'white'}),
                dcc.Graph(id='correlation-chart')
            ], md=9, className="main-content", style={
                'padding': '20px',
                'backgroundColor': 'black',
                'borderRadius': '15px',
                'height': '80%',
            })
        ], style={'margin-right': '0', 'margin-left': '0', 'backgroundColor': 'black'})
    ], fluid=True)

