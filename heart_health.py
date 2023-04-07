# notes to self - just ignore these
# These CVD risk factors include unhealthful nutrition, physical inactivity, dyslipidemia,
# hyperglycemia, high blood pressure, obesity, considerations of select populations, sex differences,
# and race/ethnicity, thrombosis/smoking, kidney dysfunction, and genetics/familial hypercholesterolemia

# what we have: activity, steps, MET, weight, heart rate

import pandas as pd

from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

def read_heartdata():

    sec_heartrate = pd.read_csv("data/heartrate_seconds_merged.csv")
    sec_heartrate.columns=['id', 'time', 'heartrate']
    min_met = pd.read_csv('data/minuteMETsNarrow_merged.csv')
    min_met.columns=['id', 'time', 'MET']
    return sec_heartrate, min_met


def manipulate_data(df1, df2):
    """
    - manipulate MET (df2) by dividing by 10, according to data dictionary
    - get minute average heartrate from df1, we only look at minute heart rate change
    return: df with id, time (every minute), heartrate, MET value """
    df2['MET'] = df2['MET'] / 10
    df2['time'] = pd.to_datetime(df2['time'], format='%m/%d/%Y %I:%M:%S %p')
    print(df2)
    # get the average heartrate in every minute
    df_avg = pd.DataFrame()
    df1['time'] = pd.to_datetime(df1['time'], format='%m/%d/%Y %I:%M:%S %p')
    df_avg['id'] = df1['id']

    df1.set_index('time', inplace=True)
    df_resampled = df1['heartrate'].resample('1T').mean()
    df_resampled = df_resampled.reset_index()
    df_resampled['id'] = df_avg['id']
    print(df_resampled)
    # not using outer join: we only evalute time when there's record for both heartrate and MET
    df_min = pd.merge(df_resampled, df2, on=['id', 'time'])
    return df_min


def heart_health_page(df):
    return dbc.Container([
        html.H1("Heart Health Tracker", className="text-center"),
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
                        id='heart-metric',
                        options=[
                            {'label': 'Heart Rate', 'value': 'heartrate'},
                            {'label': 'Metabolic Equivalents (MET) Score', 'value': 'MET'},
                        ],
                        value='Heart Rate'
                    ),
                    html.Br(),
                    html.Label('Enter User ID:'),
                    dcc.Dropdown(
                        id='user-id-sleep',
                        options=[{'label': i, 'value': i} for i in df['id'].unique()],
                        placeholder='Enter User ID', searchable=True
                    )
                ], className="bg-light sidebar", style={'border': '3px solid #000', 'height': '100%'})
            ], md=3, className="text-center"),

            # Main content
            dbc.Col([
                dcc.Graph(id='heart-stats-graph'),
                html.Div(id='heart-message', className="text-center")
                # heart rate message: just
                # "Your heart beats approximately 100,000 times per day, accelerating and slowing through periods of rest and exertion.
                # Your heart rate refers to how many times your heart beats per minute and can be an indicator of your cardiovascular health."
                # for all heart rate graphs

                # MET message:
                # Less than 5 METS is poor, 5–8 METS is fair, 9–11 METS is good, and 12 METS or more is excellent.
                # create messages in callback function - similar to "update_additional_message" callback function in main.py
            ], md=9)
        ], style={'margin-right': '0', 'margin-left': '0'})
    ], fluid=True)


def create_heart_graph(df, user_id, start_date, end_date, metric):
    """ metric: user chose in heart-metric dropdown """
    user_data = df[df['id'] == user_id]

    time_period_data = user_data[
        (user_data['time'].dt.date >= pd.to_datetime(start_date)) &
        (user_data['time'].dt.date <= pd.to_datetime(end_date))
    ]

    metric_data  = time_period_data[metric]

    fig = px.scatter(x=time_period_data, y=metric_data,
                     width=600, height=600)

    return fig



sec_heartrate, min_met = read_heartdata()
df = manipulate_data(sec_heartrate, min_met)

