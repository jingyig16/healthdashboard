import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
from data import read_data
import dash_bootstrap_components as dbc

data = read_data()
def sleep_analysis_page():
    return dbc.Container([
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div([
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
                        placeholder='Enter User ID', searchable=True
                    )
                ], className="bg-light sidebar", style={'border': '3px solid #000', 'height': '100%'})
            ], md=3, className="text-center"),

            # Main content
            dbc.Col([
                dcc.Graph(id='sleep-analysis-graph'),
                html.Div(id='sleep-message', className="text-center"),
                html.Div(id='additional-message', className="text-center")
            ], md=9)
        ], style={'margin-right': '0', 'margin-left': '0'})
    ], fluid=True)



def calculate_sleep_metrics(df, user_id, start_date, end_date):
    user_data = df[df['Id'] == user_id]

    time_period_data = user_data[
        (pd.to_datetime(user_data['ActivityDay']) >= pd.to_datetime(start_date)) &
        (pd.to_datetime(user_data['ActivityDay']) <= pd.to_datetime(end_date))
    ]

    sleep_efficiency = (time_period_data['TotalMinutesAsleep'] / time_period_data['TotalTimeInBed']) * 100
    sleep_duration = time_period_data['TotalMinutesAsleep']
    sleep_latency = time_period_data['TotalTimeInBed'] - time_period_data['TotalMinutesAsleep']

    sleep_metrics = {
        'SleepEfficiency': sleep_efficiency,
        'SleepDuration': sleep_duration,
        'SleepLatency': sleep_latency
    }

    return sleep_metrics

def create_sleep_analysis_graph(df, user_id, start_date, end_date, metric):
    sleep_metrics = calculate_sleep_metrics(df, user_id, start_date, end_date)
    selected_metric = sleep_metrics[metric]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['ActivityDay'],
        y=selected_metric,
        mode='lines+markers',
        name=metric
    ))

    fig.update_layout(
        title='Sleep Analysis',
        xaxis_title='Date',
        yaxis_title=metric
    )

    return fig
