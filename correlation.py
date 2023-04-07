# import libraries

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from data import valid_variables

from time_series import create_time_period_dropdown

# Create the dropdown menu to select a variable
category_dropdown_menu1 = dcc.Dropdown(
    id='variable-dropdown1',
    options=[],
    value=None
)

# Create the dropdown menu to select a variable
category_dropdown_menu2 = dcc.Dropdown(
    id='variable-dropdown2',
    options=[],
    value=None
)

def show_correlation(attr_1, attr_2, time_period, user_id, data):

    df1 = data[time_period][attr_1]
    df2 = data[time_period][attr_2]

    user_data1 = df1[df1['Id'] == user_id]
    user_data2 = df2[df2['Id'] == user_id]

    print(user_data1)
    print(user_data2)

    fig = px.scatter(x=user_data1[attr_1], y=user_data2[attr_2])

    return fig

def correlation_page():
    return dbc.Container([
        html.H1("Correlation Visuals", className="text-center"),
        dbc.Row([
            dbc.Col([
                html.Label("Select Time Period:"),
                create_time_period_dropdown()
            ], md=4),
            dbc.Col([
                html.Label("Select a Visualization:"),
                category_dropdown_menu1,
            ], md=4),
            dbc.Col([
                html.Label("Select a Visualization:"),
                category_dropdown_menu2,
            ], md=4),
            dbc.Col([
                html.Label("Enter Your User ID:"),
                dcc.Input(id='user-id', type='number', placeholder='Enter User ID'),
            ], md=4)
        ], className='my-3'),
        dcc.Graph(id='correlation-chart')
    ])
