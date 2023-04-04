import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from home import homepage
from time_series import create_time_period_dropdown, category_dropdown_menu, create_time_series, time_series_page
from data import valid_variables


# Function to read the data
def read_data():
    daily_activity = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")
    daily_sleep = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")
    daily_weight = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/weightLogInfo_merged.csv")
    hourly_calories = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/hourlyCalories_merged.csv")
    hourly_intensities = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/hourlyIntensities_merged.csv")
    hourly_steps = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/hourlySteps_merged.csv")
    minute_calories_narrow = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteCaloriesNarrow_merged.csv")
    minute_intensities_narrow = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteIntensitiesNarrow_merged.csv")
    minute_steps_narrow = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteStepsNarrow_merged.csv")
    minute_sleep = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteSleep_merged.csv")
    second_heartrate = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/heartrate_seconds_merged.csv")

    # Renaming column names for consistency over dataframes
    daily_activity = daily_activity.rename(columns={'ActivityDate': 'ActivityDay'})
    daily_sleep = daily_sleep.rename(columns={'SleepDay': 'ActivityDay'})
    daily_weight = daily_weight.rename(columns={'Date': 'ActivityDay'})
    minute_sleep = minute_sleep.rename(columns={'date': 'ActivityMinute'})
    second_heartrate = second_heartrate.rename(columns={'Time': 'ActivitySecond'})

    # Defining the variables and the dataframe it needs to be pulled from
    data = {
        "D": {
            "TotalSteps": daily_activity,
            "TotalDistance": daily_activity,
            "TrackerDistance": daily_activity,
            "LoggedActivitiesDistance": daily_activity,
            "VeryActiveDistance": daily_activity,
            "ModeratelyActiveDistance": daily_activity,
            "LightActiveDistance": daily_activity,
            "SedentaryActiveDistance": daily_activity,
            "VeryActiveMinutes": daily_activity,
            "FairlyActiveMinutes": daily_activity,
            "LightlyActiveMinutes": daily_activity,
            "SedentaryMinutes": daily_activity,
            "Calories": daily_activity,
            "TotalMinutesAsleep": daily_sleep,
            "TotalTimeInBed": daily_sleep,
            "WeightKg": daily_weight,
            "WeightPounds": daily_weight,
            "BMI": daily_weight
        },
        "H": {
            "Calories": hourly_calories,
            "TotalIntensity": hourly_intensities,
            "StepTotal": hourly_steps
        },
        "M": {
            "Steps": minute_steps_narrow,
            "Calories": minute_calories_narrow,
            "Intensity": minute_intensities_narrow,
            "value": minute_sleep
        },
        "S": {
            "Value": second_heartrate
        }
    }

    return data


# Reading the data
data = read_data()

# Initializing the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Defining navigation bar for features of dashboard
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Home", href="/home", className="nav-link")),
        dbc.NavItem(dcc.Link("Time Series Visuals", href="/time-series", className="nav-link")),
        dbc.NavItem(dcc.Link("Correlation Exploration", href="/correlation", className="nav-link")),
        dbc.NavItem(dcc.Link("Demographic Comparison", href="/demographic", className="nav-link")),
        dbc.NavItem(dcc.Link("Health Risk Assessment", href="/health-risk", className="nav-link")),
    ],
    brand="Fitbit Insights Dashboard",
    brand_href="/",
    sticky="top",
)

# Designing app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


# Callback for page navigation
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home':
        return homepage()
    elif pathname == '/time-series':
        return time_series_page()
        # [Add more elif conditions for other pages here]
    else:
        return homepage()



# Callback to update the time series chart
@app.callback(Output('time-series-chart', 'figure'),
              Input('variable-dropdown', 'value'),
              Input('time-period-dropdown', 'value'),
              Input('user-id', 'value'))
def update_time_series(variable, time_period, user_id):
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

# Callback to update category dropdown
@app.callback(Output('variable-dropdown', 'options'),
              Input('time-period-dropdown', 'value'))
def update_category_dropdown(time_period):
    options = [{'label': v, 'value': v} for v in valid_variables[time_period]]
    return options


# Update the app's config to suppress_callback_exceptions
app.config.suppress_callback_exceptions = True


if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
