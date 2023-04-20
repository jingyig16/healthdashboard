"""
Anoushka Bhatia, Xi Chen, Jai Gollapudi, Jingyi Gong, Krishi Patel, Shreya Thalvayapati
DS3500 Final Project: Fitbit Insights Dashboard
4/19/2023
main.py: All callback functions
Github repo: https://github.com/jingyig16/healthdashboard
"""

# Importing libraries
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from data import read_data
from home import homepage
from sleep_analysis import sleep_analysis_page, calculate_sleep_metrics, create_sleep_analysis_graph

from time_series import category_dropdown_menu, create_time_series, time_series_page
from correlation import create_corr, correlation_page, interpret_r_score
from data import valid_variables
from heart_health import heart_health_page, create_heart_graph, df


# Reading the data
data = read_data()

# Using external stylesheets for app layout
external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css']

# Initializing the app with external_stylesheets
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Defining navigation bar for features of dashboard
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Home", href="/home", className="nav-link",
                             style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Time Series Visuals", href="/time-series", className="nav-link",
                             style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Correlation Exploration", href="/correlation", className="nav-link",
                             style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Sleep Analysis", href="/sleep-analysis", className="nav-link",
                             style={'color': 'white'})),
        dbc.NavItem(dcc.Link("Heart Health Tracker", href="/heart-health", className="nav-link",
                             style={'color': 'white'})),
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
        return heart_health_page(df)
    elif pathname == '/correlation':
        return correlation_page()
    else:
        return homepage()


################################################
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
    options = [{'label': v, 'value': v} for v in valid_variables[time_period]]
    category_dropdown_menu.options = options

    # Check if the selected variable is valid for the selected time period
    if variable is None or variable not in valid_variables[time_period]:
        variable = valid_variables[time_period][0]

    # Check if the selected user ID is valid for the selected variable and time period
    data_df = data[time_period][variable]
    if user_id not in data_df['Id'].unique():
        user_id = data_df['Id'].iloc[0]

    return create_time_series(variable, time_period, user_id, data)


# Callback to update the user id options in time_series
@app.callback(Output('user-id-ts', 'options'),
              Input('variable-dropdown', 'value'),
              Input('time-period-dropdown1', 'value'))
def update_user_id_options(variable, time_period):
    """
    Updates user id dropdown
    :param variable: User selected variable
    :param time_period: User selected time period
    :return: user id drop down options
    """
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


# Callback to reset variable and user id dropdowns when new time period is selected
@app.callback(
    Output('variable-dropdown', 'value'),
    Output('user-id-ts', 'value'),
    Input('time-period-dropdown1', 'value')
)
def reset_dropdowns(time_period):
    """
    Resets dropdown values when new time period is selected
    :param time_period: User selected time period
    :return: None for variable and user id
    """
    return None, None

################################################
# Sleep Analysis Callbacks


# Callback to update the sleep analysis graph
@app.callback(Output('sleep-analysis-graph', 'figure'),
              Input('user-id-sleep', 'value'),
              Input('date-range', 'start_date'),
              Input('date-range', 'end_date'),
              Input('sleep-metric', 'value'))
def update_sleep_analysis_graph(user_id, start_date, end_date, metric):
    """
    Updates sleep analysis graph
    :param user_id: Users ID
    :param start_date: Selected start date
    :param end_date: Selected end date
    :param metric: Sleep metric chosen
    :return: Sleep analysis graph
    """
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
    """
    Updates sleep message
    :param user_id: Users ID
    :param start_date: Selected start date
    :param end_date: Selected end date
    :param metric: Sleep metric chosen
    :return: Sleep message to be displayed
    """
    if user_id is None or start_date is None or end_date is None:
        return ""

    sleep_metrics = calculate_sleep_metrics(data['D']['TotalMinutesAsleep'], user_id, start_date, end_date)
    avg_metric = sleep_metrics[metric].mean()

    threshold = {
        'SleepEfficiency': [85, 90],
        'SleepDuration': [420, 480],
        'SleepLatency': [15, 30]
    }

    # Suggestion for sleep latency
    if metric == 'SleepLatency':
        if avg_metric > threshold[metric][0]:
            message = f'Poor {metric}: Your average {metric} is above the recommended range of  ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Consider incorporating relaxation  ' \
                      f' techniques, avoid caffeine and create a consistent bedtime routine to help signal to your  ' \
                      f'body that its time to sleep.'
        elif threshold[metric][0] <= avg_metric <= threshold[metric][1]:
            message = f'Fair {metric}: Your average {metric} is within the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Keep up the good work! Continue' \
                      f' with your current sleep habits and consider experimenting with additional relaxation ' \
                      f'techniques or adjusting your sleep environment to further improve sleep latency.'
        else:
            message = f'Good {metric}: Your average {metric} is below the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Great job! You are falling asleep' \
                      f' quickly. Continue maintaining your healthy sleep habits to ensure a consistent sleep onset.'
    # Suggestion for sleep duration
    elif metric == 'SleepDuration':
        if avg_metric < threshold[metric][0]:
            message = f'Poor {metric}: Your average {metric} is below the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Aim to get at least 7 hours of ' \
                      f'sleep per night. Establish a regular sleep schedule, avoid consuming caffeine or alcohol ' \
                      f'close to bedtime, and ensure a quiet and comfortable sleep environment.'
        elif threshold[metric][0] <= avg_metric <= threshold[metric][1]:
            message = f'Fair {metric}: Your average {metric} is within the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Good job! You are meeting the' \
                      f' recommended sleep duration. Continue with your current sleep habits and make any' \
                      f' adjustments as needed to maintain this sleep duration.'
        else:
            message = f'Good {metric}: Your average {metric} is above the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. While you are getting sufficient' \
                      f' sleep, its essential to monitor your daytime alertness and energy levels. If you feel overly' \
                      f' tired or groggy during the day, consider consulting a healthcare professional'
    # Suggestion for sleep latency
    else:
        if avg_metric < threshold[metric][0]:
            message = f'Poor {metric}: Your average {metric} is below the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Consider establishing a consistent' \
                      f' sleep schedule, creating a comfortable sleep environment, and avoiding caffeine and' \
                      f' electronics before bed to improve sleep efficiency.'
        elif threshold[metric][0] <= avg_metric <= threshold[metric][1]:
            message = f'Fair {metric}: Your average {metric} is within the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Keep maintaining your current sleep' \
                      f' habits but try to further improve your sleep routine by incorporating relaxation' \
                      f' techniques, such as meditation or deep breathing exercises, before bed.'
        else:
            message = f'Good {metric}: Your average {metric} is above the recommended range of ' \
                      f'{threshold[metric][0]} to {threshold[metric][1]} minutes. Great job! Continue maintaining' \
                      f' your healthy sleep habits to ensure consistent, high-quality sleep.'

    return message


# Callback to update the user id options in sleep_analysis
@app.callback(Output('user-id-sleep', 'options'),
              Input('daily_sleep', 'data'),
              Input('date-range', 'start_date'),
              Input('date-range', 'end_date'),
              Input('sleep-metric', 'value'))
def update_user_id_options(daily_sleep_data, start_date, end_date, metric):
    """
    Updates user id dropdown
    :param daily_sleep_data: Daily sleep data
    :param start_date: Selected start date
    :param end_date: Selected end date
    :param metric: Selected sleep metric
    :return: user id options  in dropdown
    """
    if daily_sleep_data is None or start_date is None or end_date is None or metric is None:
        return []

    df = pd.DataFrame(daily_sleep_data)

    # Filter user IDs based on selected date range and metric
    filtered_user_ids = []
    for user_id in df['Id'].unique():
        sleep_metrics = calculate_sleep_metrics(df, user_id, start_date, end_date)
        if not sleep_metrics[metric].empty:
            filtered_user_ids.append(user_id)

    user_ids = [{'label': i, 'value': i} for i in filtered_user_ids]
    return user_ids


# Callback to generate info on sleep metric chosen
@app.callback(
    Output('additional-message', 'children'),
    Input('user-id-sleep', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('sleep-metric', 'value'))
def update_additional_message(user_id, start_date, end_date, metric):
    """
    Updates suggestion
    :param user_id: Users ID
    :param start_date: Selected start date
    :param end_date: Selected end date
    :param metric: Sleep metric chosen
    :return: Sleep message to be displayed
    """
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

################################################
# Correlation Exploration Callbacks


# Update the variable dropdowns based on the time period selection and first variable
@app.callback(
    [Output('variable-dropdown1', 'options'),
     Output('variable-dropdown2', 'options')],
    [Input('time-period-dropdown2', 'value'),
     Input('variable-dropdown1', 'value')]
)
def update_variable_dropdowns(time_period, first_variable):
    """
    Updates variable dropdown options
    :param time_period:
    :param first_variable:
    :return:  variable dropdown options
    """
    variable_options = [{'label': var, 'value': var} for var in valid_variables[time_period]]

    if first_variable is None:
        return variable_options, []

    first_variable_length = len(data[time_period][first_variable])
    variable_options2 = [
        {'label': var, 'value': var}
        for var in valid_variables[time_period]
        if len(data[time_period][var]) == first_variable_length
    ]

    return variable_options, variable_options2


# Update the user id options in time_series
@app.callback(Output('user-id-corr', 'options'),
              [Input('variable-dropdown1', 'value'),
               Input('time-period-dropdown2', 'value')])
def update_user_id_options(variable, time_period):
    """
    Updates variable dropdown options for variable 2 based on variable 1
    :param variable: Chosen variable1
    :param time_period: Chosen time period
    :return: Updates variable dropdown options for variable 2
    """
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
    """
    Updates the correlation chart based on user inputs
    :param time_period: Chosen time period
    :param variable1: Chosen variable
    :param variable2: Chosen variable
    :param user_id: Users ID
    :return: Correlation chart with line of best fit and correlation coef
    """
    if not (time_period and variable1 and variable2 and user_id):
        return go.Figure()

    fig, r_value = create_corr(variable1, variable2, time_period, user_id, data)
    return fig

# Callback on reset dropdowns for future, new selections
@app.callback(
    [Output('variable-dropdown1', 'value'),
     Output('variable-dropdown2', 'value'),
     Output('user-id-corr', 'value')],
    [Input('time-period-dropdown2', 'value'),
     Input('variable-dropdown1', 'value')]
)
def reset_dropdowns_on_change(time_period_value, variable1_value):
    """
    Checks which callback was triggered and resets rest of dropdowns accordingly
    :param time_period_value: Selected time period
    :param variable1_value: Selected variable 1
    :return: dash.no_update indicating there's no updates, or None
    """
    ctx = dash.callback_context

    # Check which input triggered the callback
    if ctx.triggered:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        input_id = None

    if input_id == 'time-period-dropdown2':
        return None, None, None
    elif input_id == 'variable-dropdown1':
        return dash.no_update, None, None
    else:
        return dash.no_update, dash.no_update, dash.no_update


# Callback on update r scores after graph changes
@app.callback(
    Output('r-score-interpretation', 'children'),
    [Input('time-period-dropdown2', 'value'),
     Input('variable-dropdown1', 'value'),
     Input('variable-dropdown2', 'value'),
     Input('user-id-corr', 'value')]
)
def update_r_score_interpretation(time_period, variable1, variable2, user_id):
    """
    Updates the interpretation message on r score between chosen variables
    :param time_period: Chosen time period
    :param variable1: Chosen variable 1
    :param variable2: Chosen variable 2
    :param user_id: Users ID
    :return: Interpretation message on r score between chosen variables
    """
    if not (time_period and variable1 and variable2 and user_id):
        return ""

    fig, r_value = create_corr(variable1, variable2, time_period, user_id, data)
    if r_value is None:
        return "Cannot calculate a linear regression if all x values are identical"

    interpretation = interpret_r_score(r_value)
    return f"R Score Interpretation: {interpretation} (r = {r_value:.2f})"


################################################
# Heart Health Callbacks
# Callback function to update heart message
@app.callback(
    Output('heart-message', 'children'),
    [Input('heart-metric', 'value')]
)
def update_heart_message(metric):
    """
    Updates heart health messages based on metric chosen
    :param metric: Chosen metric
    :return: heart health messages based on metric chosen
    """
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
    [Input('user-id-heart', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('heart-metric', 'value')]
)
def update_heart_graph(user_id, start_date, end_date, metric):
    """
    Updates the heart health graoh based iin the users inputs
    :param user_id: Users ID
    :param start_date: Chosen start date
    :param end_date: Chosen end date
    :param metric: Chosen heart health metric
    :return: Heart health graph
    """
    if user_id is None or start_date is None or end_date is None:
        return dash.no_update, dash.no_update

    fig = create_heart_graph(df, user_id, start_date, end_date, metric)

    met_message = ""

    if metric == 'MET':
        met_message = "Metabolic Equivalents (METs) measure the energy cost of physical activities. 1 MET " \
                      "is defined as the amount of oxygen consumed while sitting at rest and is equal to " \
                      "3.5 ml O2/kg/min. " \
                      "A higher MET score indicates a higher intensity activity. Less than 5 METs is poor, " \
                      "5–8 METs is fair, 9–11 METs is good, and 12 METs or more is excellent."

    return fig, met_message


# Update the app's config to suppress_callback_exceptions
app.config.suppress_callback_exceptions = True


# Running the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)


