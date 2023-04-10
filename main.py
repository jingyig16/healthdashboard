import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from data import read_data, valid_variables
from home import homepage
from time_series import category_dropdown_menu, create_time_series, time_series_page
from sleep_analysis import sleep_analysis_page, calculate_sleep_metrics, create_sleep_analysis_graph

from correlation import correlation_page, create_corr
from time_series import create_time_period_dropdown1, category_dropdown_menu, create_time_series, time_series_page
from correlation import create_time_period_dropdown2, variable_dropdown_menu1, variable_dropdown_menu2, create_corr, correlation_page
from data import valid_variables
from heart_health import heart_health_page, create_heart_graph, df, read_heartdata, manipulate_data, update_met_message


# Reading the data
data = read_data()

# Initializing the app with external_stylesheets
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Defining navigation bar for features of dashboard
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Home", href="/home", className="nav-link", style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Time Series Visuals", href="/time-series", className="nav-link", style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Correlation Exploration", href="/correlation", className="nav-link", style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Sleep Analysis", href="/sleep-analysis", className="nav-link", style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Health Risk Assessment", href="/heart-health", className="nav-link", style={'color': 'white'})),
    ],
    brand="Fitbit Insights Dashboard",
    brand_href="/",
    sticky="top",
    color="dark",
    dark=True
)

# Designing app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
], style={'backgroundColor': 'black', 'height': '100vh'})



# Callback for page (feature) navigation
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """ Redirects the user to the page that the user has clicked on

    :param pathname: The hypertext reference of the specific page
    :return: The specific page (Home page is default)
    """
    # Checking pathname and returning page accordingly
    if pathname == '/home':
        return homepage()
    elif pathname == '/time-series':
        return time_series_page()
    elif pathname == '/sleep-analysis':
        return sleep_analysis_page()
    elif pathname == '/heart-health':
        return heart_health_page()
    elif pathname == '/correlation':
        return correlation_page()
    else:
        return homepage()


################################################################################################
# Time Series Callbacks

# Callback to update the time series chart
@app.callback(Output('time-series-chart', 'figure'),
              Input('variable-dropdown', 'value'),
              Input('time-period-dropdown1', 'value'),
              Input('user-id-ts', 'value'))
def update_time_series(variable, time_period, user_id):
    """ Checks user ID, updates options in dropdown menu, and creates a
        new time series image based on updated inputs.

    :param variable: The variable the user wants to explore
    :param time_period: The time period the user chooses
    :param user_id: The user's ID number
    :return: Updated Plotly linegraph figure
    """
    if user_id is None:
        return {}
    # Update the options in the category_dropdown_menu
    if time_period == 'D':
        options = [{'label': v, 'value': v} for v in valid_variables['D']]
    elif time_period == 'H':
        options = [{'label': v, 'value': v} for v in valid_variables['H']]
    elif time_period == 'M':
        options = [{'label': v, 'value': v} for v in valid_variables['M']]
    elif time_period =='S':
        options = [{'label': v, 'value': v} for v in valid_variables['S']]
    else:
        options = []
    category_dropdown_menu.options = options

    # Check if the selected variable is valid for the selected time period
    if variable not in valid_variables[time_period]:
        variable = valid_variables[time_period][0]

    return create_time_series(variable, time_period, user_id, data)


# Callback to update the user id options in time_series
@app.callback(Output('user-id-ts', 'options'),
              Input('variable-dropdown', 'value'),
              Input('time-period-dropdown1', 'value'))
def update_user_id_options(variable, time_period):
    if variable is None:
        return []

    # Get the DataFrame for the selected variable and time period
    data_df = data[time_period][variable]

    # Extract unique user IDs from the DataFrame
    unique_user_ids = data_df['Id'].unique()

    # Convert the unique user IDs into the appropriate options format for the dropdown component
    options = [{'label': str(user_id), 'value': user_id} for user_id in unique_user_ids]

    return options


# Callback to update category dropdown according
# to time period selected
@app.callback(Output('variable-dropdown', 'options'),
              Input('time-period-dropdown1', 'value'))
def update_category_dropdown(time_period):
    """ Updates the category dropdown menu based on user inputs

    :param time_period: The time period the user chooses
    :return: Updated category dropdown menu
    """
    options = [{'label': v, 'value': v} for v in valid_variables[time_period]]
    return options

##########################################################################################
# Sleep Analysis Callbacks

# Callback to update the sleep analysis graph
@app.callback(Output('sleep-analysis-graph', 'figure'),
              Input('user-id-sleep', 'value'),
              Input('date-range', 'start_date'),
              Input('date-range', 'end_date'),
              Input('sleep-metric', 'value'))
def update_sleep_analysis_graph(user_id, start_date, end_date, metric):
    if user_id is None or start_date is None or end_date is None:
        return {}
    return create_sleep_analysis_graph(data['D']['TotalMinutesAsleep'], user_id, start_date, end_date, metric)


# Callback to update the evaluation and suggestion, based on
# thresholds
@app.callback(
    Output('sleep-message', 'children'),
    Input('user-id-sleep', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('sleep-metric', 'value'))
def update_sleep_message(user_id, start_date, end_date, metric):
    if user_id is None or start_date is None or end_date is None:
        return ""

    sleep_metrics = calculate_sleep_metrics(data['D']['TotalMinutesAsleep'], user_id, start_date, end_date)
    avg_metric = sleep_metrics[metric].mean()
    threshold = {
        'SleepEfficiency': [85, 90],
        'SleepDuration': [420, 480],
        'SleepLatency': [15, 30]
    }

    if metric == 'SleepLatency':
        if avg_metric > threshold[metric][0]:
            message = f'Poor {metric}: Your average {metric} is above the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
        elif threshold[metric][0] <= avg_metric <= threshold[metric][1]:
            message = f'Fair {metric}: Your average {metric} is within the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
        else:
            message = f'Good {metric}: Your average {metric} is below the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
    elif metric == 'SleepDuration':
        if avg_metric < threshold[metric][0]:
            message = f'Poor {metric}: Your average {metric} is below the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
        elif threshold[metric][0] <= avg_metric <= threshold[metric][1]:
            message = f'Fair {metric}: Your average {metric} is within the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
        else:
            message = f'Good {metric}: Your average {metric} is above the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
    else:
        if avg_metric < threshold[metric][0]:
            message = f'Poor {metric}: Your average {metric} is below the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
        elif threshold[metric][0] <= avg_metric <= threshold[metric][1]:
            message = f'Fair {metric}: Your average {metric} is within the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'
        else:
            message = f'Good {metric}: Your average {metric} is above the recommended range of {threshold[metric][0]} to {threshold[metric][1]} minutes.'

    return message

# Callback to update the user id options in sleep_analysis
@app.callback(Output('user-id-sleep', 'options'),
              Input('daily_sleep', 'data'))
def update_user_id_options(daily_sleep_data):
    if daily_sleep_data is None:
        return []

    df = pd.DataFrame(daily_sleep_data)
    user_ids = [{'label': i, 'value': i} for i in df['Id'].unique()]
    return user_ids

# Callback to generate info on sleep metric chosen
@app.callback(
    Output('additional-message', 'children'),
    Input('user-id-sleep', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('sleep-metric', 'value'))
def update_additional_message(user_id, start_date, end_date, metric):
    if user_id is None or start_date is None or end_date is None or metric is None:
        return ""

    # Your custom logic to generate the additional message based on the selected metric
    if metric == 'SleepEfficiency':
        message = f"Sleep efficiency is the percentage of time you are actually asleep while in bed. "
    elif metric == 'SleepDuration':
        message = f"Sleep duration refers to the total amount of time you spend asleep. "
    elif metric == 'SleepLatency':
        message = f"Sleep latency is the time it takes to fall asleep after going to bed. "


    return message

##########################################################################################
# Correlation Exploration Callbacks

# Update the variable dropdowns based on the time period selection
@app.callback(
    [Output('variable-dropdown1', 'options'),
     Output('variable-dropdown2', 'options')],
    [Input('time-period-dropdown2', 'value')]
)
def update_variable_dropdowns(time_period):
    variable_options = [{'label': var, 'value': var} for var in valid_variables[time_period]]
    return variable_options, variable_options

# Update the user id options in time_series
@app.callback(Output('user-id-corr', 'options'),
              [Input('variable-dropdown1', 'value'),
               Input('time-period-dropdown2', 'value')])
def update_user_id_options(variable, time_period):
    if variable is None or time_period is None:
        return []

    # Get the DataFrame for the selected variable and time period
    data_df = data[time_period][variable]

    # Extract unique user IDs from the DataFrame
    unique_user_ids = data_df['Id'].unique()

    # Convert the unique user IDs into the appropriate options format for the dropdown component
    options = [{'label': str(user_id), 'value': user_id} for user_id in unique_user_ids]

    return options

# Create the time series chart based on user input
@app.callback(
    Output('correlation-chart', 'figure'),
    [Input('time-period-dropdown2', 'value'),
     Input('variable-dropdown1', 'value'),
     Input('variable-dropdown2', 'value'),
     Input('user-id-corr', 'value')]
)
def update_corr_chart(time_period, variable1, variable2, user_id):
    if not (time_period and variable1 and variable2 and user_id):
        return go.Figure()

    return create_corr(variable1, variable2, time_period, user_id, data)

#########################################################################################################
# Heart Health Callbacks
# Callback function to update heart message
@app.callback(
    Output('heart-message', 'children'),
    [Input('heart-metric', 'value')]
)
def update_heart_message(metric):
    heart_message = ""

    if metric == 'heartrate':
        heart_message = "Your heart beats approximately 100,000 times per day, accelerating and slowing " \
                        "through periods of rest and exertion. " \
                        "Your heart rate refers to how many times your heart beats per minute and can be an " \
                        "indicator of your cardiovascular health."

    return heart_message

# Callback for Heart Health Tracker
@app.callback(
    [Output('heart-stats-graph', 'figure'),
     Output('met-message', 'children')],
    [Input('user-id-sleep', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('heart-metric', 'value')]
)
def update_heart_graph(user_id, start_date, end_date, metric):
    if user_id is None or start_date is None or end_date is None:
        return dash.no_update, dash.no_update

    fig = create_heart_graph(df, user_id, start_date, end_date, metric)

    met_message = ""

    if metric == 'MET':
        avg_mets = df[df['id'] == user_id]['MET'].mean()
        met_message = "Metabolic Equivalents (METs) measure the energy cost of physical activities. " \
                      "A higher MET score indicates a higher intensity activity. " + update_met_message(avg_mets)

    return fig, met_message


# Update the app's config to suppress_callback_exceptions
app.config.suppress_callback_exceptions = True


# Running the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8053)


