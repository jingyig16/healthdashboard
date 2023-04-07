import dash_bootstrap_components as dbc
from dash import html



def homepage():
    """ Defines the layout for the home page in the dashboard
        with headings, paragraphs, and images.

    :return: The layout for the home page in the dashboard
    """
    return dbc.Container([
        html.H1("Welcome to Fitbit Insights Dashboard", className="text-center"),
        html.P("This is the home page of the Fitbit Insights Dashboard.", className="text-center"),
        html.Div([
            html.Img(src="fitbit_image.png", style={'height': '50%', 'width': '50%'})
        ], className="text-center")
    ])
