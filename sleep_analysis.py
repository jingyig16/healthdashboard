"""
Anoushka Bhatia, Xi Chen, Jai Gollapudi, Jingyi Gong, Krishi Patel, Shreya Thalvayapati
DS3500 Final Project: Fitbit Insights Dashboard
4/19/2023
sleep_analysis.py: individual file for Sleep Analysis
Github repo: https://github.com/jingyig16/healthdashboard
"""

# Importing libraries
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from data import read_data
import dash_bootstrap_components as dbc

# Reading data
data = read_data()


def calculate_sleep_metrics(df, user_id, start_date, end_date):
    """ Calculates sleep metrics: sleep efficiency, sleep duration, sleep latency
    :param df: The dataframe to extract the data from
    :param user_id: The users ID
    :param start_date: The start date chosen on the dashboard
    :param end_date: The end date chosen on the dashboard
    :return: Dictionary of sleep metrics
    """
    # Selecting user data
    user_data = df[df['Id'] == user_id]

    # Selecting data withing data range
    time_period_data = user_data[
        (pd.to_datetime(user_data['ActivityDay']) >= pd.to_datetime(start_date)) &
        (pd.to_datetime(user_data['ActivityDay']) <= pd.to_datetime(end_date))
    ]

    # Calculating sleep metrics
    sleep_efficiency = (time_period_data['TotalMinutesAsleep'] / time_period_data['TotalTimeInBed']) * 100
    sleep_duration = time_period_data['TotalMinutesAsleep']
    sleep_latency = time_period_data['TotalTimeInBed'] - time_period_data['TotalMinutesAsleep']

    # Saving sleep metric results in a dict
    sleep_metrics = {
        'SleepEfficiency': sleep_efficiency,
        'SleepDuration': sleep_duration,
        'SleepLatency': sleep_latency
    }

    return sleep_metrics


def create_sleep_analysis_graph(df, user_id, start_date, end_date, metric):
    """ Extracts data based on user Id, date range, metric, and produces a
    line plot of the daily average

    :param df: The dataframe to extract the data from
    :param user_id: The users ID
    :param start_date: The start date chosen on the dashboard
    :param end_date: The end date chosen on the dashboard
    :param metric: The sleep metric that the user has chosen to see
    :return: Plotly go figure
    """
    # Calculating sleep metrics and filtering selected metric
    sleep_metrics = calculate_sleep_metrics(df, user_id, start_date, end_date)
    selected_metric = sleep_metrics[metric]

    # Initializing go.figure
    fig = go.Figure()

    # Adding scatter plot
    fig.add_trace(go.Scatter(
        x=df['ActivityDay'],
        y=selected_metric,
        mode='lines+markers',
        name=metric
    ))

    # Setting title and axes names
    fig.update_layout(
        title=f'{metric} from {start_date} to {end_date}',
        xaxis_title='Date',
        yaxis_title=metric
    )

    return fig


# Designing layout of the page
def sleep_analysis_page():
    """ Defines the layout for the sleep analysis page in the dashboard
        with headings, multiple rows and columns, and graphs.

    :return: The layout for the sleep analysis page in the dashboard
    """
    return dbc.Container([
        html.Br(),
        dcc.Store(id='daily_sleep', data=data['D']['TotalMinutesAsleep'].to_dict()),
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div([
                    html.H5("Filters"),
                    html.Hr(),
                    html.Label('Select a time period:'),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date_placeholder_text='Start Date',
                        end_date_placeholder_text='End Date',
                        min_date_allowed=pd.to_datetime('2016-04-12'),
                        max_date_allowed=pd.to_datetime('2016-05-12')
                    ),
                    html.Br(),
                    html.Label('Select a metric:'),
                    dcc.Dropdown(
                        id='sleep-metric',
                        options=[
                            {'label': 'Sleep Efficiency', 'value': 'SleepEfficiency'},
                            {'label': 'Sleep Duration', 'value': 'SleepDuration'},
                            {'label': 'Sleep Latency', 'value': 'SleepLatency'}
                        ],
                        value='SleepEfficiency'
                    ),
                    html.Br(),
                    html.Label('Enter User ID:'),
                    dcc.Dropdown(
                        id='user-id-sleep',
                        options=[{'label': i, 'value': i} for i in data['D']['TotalMinutesAsleep']['Id'].unique()],
                        placeholder='Enter User ID', searchable=True),
                    html.Br(),
                    html.Div(id='sleep-message', className="text-center", style={'color': 'black'})
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
                html.Div([
                    html.H1("Sleep Analysis", className="text-center", style={'color': 'white'}),
                    html.Div([
                        dcc.Graph(id='sleep-analysis-graph')
                    ], style={
                        'padding': '20px',
                        'height': '100%',
                    }),
                ], style={
                    'padding': '20px',
                    'backgroundColor': 'black',
                    'borderRadius': '15px',
                    'height': '10%',
                }),
                html.Div(id='additional-message', className="text-center", style={'color': 'white'})
            ], md=9)
        ], style={'margin-right': '0', 'margin-left': '0'})
    ], fluid=True)
