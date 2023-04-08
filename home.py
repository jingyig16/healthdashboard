import dash_bootstrap_components as dbc
from dash import html

def homepage():
    """ Defines the layout for the home page in the dashboard
        with headings, paragraphs, and images.

    :return: The layout for the home page in the dashboard
    """
    return dbc.Container([
        html.Br(),
        html.H1("Welcome to Fitbit Insights Dashboard", className="text-center", style={'color': 'white'}),
        html.P("This is the home page of the Fitbit Insights Dashboard.", className="text-center", style={'color': 'white'}),
        html.Div([
            html.Img(src="https://i.postimg.cc/y6XfBjhV/fitbit-image.png", alt='fitbit watch picture', style={'height': '25%', 'width': '25%'})
        ], className="text-center")
    ], style={'backgroundColor': 'black'})
