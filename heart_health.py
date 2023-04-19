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
    """ Reads the heart data into respective dataframes
    :return: heart rate and met dataframes
    """
    sec_heartrate = pd.read_csv("data/heartrate_seconds_merged.csv")
    sec_heartrate.columns=['id', 'time', 'heartrate']
    min_met = pd.read_csv('data/minuteMETsNarrow_merged.csv')
    min_met.columns=['id', 'time', 'MET']
    return sec_heartrate, min_met


def manipulate_data(df1, df2):
    """ Manipulates MET (df2) by dividing by 10, according to data dictionary,
    Gets minute average heartrate from df1, we only look at minute heart rate change

    :param df1: Dataframe
    :param df2: Dataframe
    :return: df with id, time (every minute), heartrate, MET value
    """


    df2['MET'] = df2['MET'] / 10
    df2['time'] = pd.to_datetime(df2['time'], format='%m/%d/%Y %I:%M:%S %p')
    # get the average heartrate in every minute


    df1['time'] = pd.to_datetime(df1['time'], format='%m/%d/%Y %I:%M:%S %p')
    df = df1.copy()
    df['id'] = df['id'].astype(int)
    df_resampled = df.groupby(['id', pd.Grouper(key='time', freq='1Min')])['heartrate'].mean()
    df_resampled = df_resampled.reset_index()
    df_resampled['time'] = df_resampled['time'].dt.round('1min')
    df_min = df_resampled.merge(df2, on=['id', 'time'])
    return df_min


def heart_health_page(df):
    """ Defines the layout for the heart health page in the dashboard
        with headings, multiple rows and columns, and graphs.

    :param df: Required Dataframe to select column from
    :return: The layout for the heart health page in the dashboard
    """
    return dbc.Container([
        html.Br(),
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.Div([
                    html.H5("Filters"),
                    html.Hr(),
                    html.Label("Select a time period:"),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date_placeholder_text='Start Date',
                        end_date_placeholder_text='End Date',
                        min_date_allowed=pd.to_datetime('2016-04-12'),
                        max_date_allowed=pd.to_datetime('2016-05-12')
                    ),
                    html.Br(),
                    html.Label("Select a metric:"),
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
                        id='user-id-heart',
                        options=[{'label': i, 'value': i} for i in df['id'].unique()],
                        placeholder='Enter User ID', searchable=True
                    ),
                    html.P("If nothing shows on the graph, it means that there's no data recorded "
                           "during the time period selected.")
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
                html.H1("Heart Health Tracker", className="text-center", style={'color':'white'}),
                html.Div(id='heart-message', className="text-center", style={'color':'white'}),
                html.Div(id='met-message', className="text-center", style={'color':'white'}),
                dcc.Graph(id='heart-stats-graph')
            ], md=9, className='main-content', style={
                'padding': '20px',
                'backgroundColor': 'black',
                'borderRadius': '15px',
                'height': '80%',
            })
        ], style={'margin-right': '0', 'margin-left': '0', 'backgroundColor': 'black'})
    ], fluid=True)



def create_heart_graph(df, user_id, start_date, end_date, metric):
    """ Extracts data based, on user ID, date range, and metric,
    and produces scatter plot of metric

    :param df: The dataframe to extract the data from
    :param user_id: The users ID
    :param start_date: The start date chosen on the dashboard
    :param end_date: The end date chosen on the dashboard
    :param metric: The heart health metric that the user has chosen to see
    :return: Plotly go figure
    """
    """ metric: user chose in heart-metric dropdown """
    user_data = df[df['id'] == user_id]

    time_period_data = user_data[
        (user_data['time'].dt.date >= pd.to_datetime(start_date)) &
        (user_data['time'].dt.date <= pd.to_datetime(end_date))
    ]

    metric_data = time_period_data[metric]

    fig = px.scatter(time_period_data, x='time', y=metric)

    return fig




sec_heartrate, min_met = read_heartdata()
df = manipulate_data(sec_heartrate, min_met)


