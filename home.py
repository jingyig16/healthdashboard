import dash_bootstrap_components as dbc
from dash import html


# Defining the homepage
def homepage():
    return dbc.Container([
        html.H1("Welcome to Fitbit Insights Dashboard", className="text-center"),
        html.P("This is the home page of the Fitbit Insights Dashboard."),
        html.P("Use the navigation bar above to access other pages."),
    ])
