"""
Anoushka Bhatia, Xi Chen, Jai Gollapudi, Jingyi Gong, Krishi Patel, Shreya Thalvayapati
DS3500 Final Project: Fitbit Insights Dashboard
4/19/2023
home.py: individual file for homepage
Github repo: https://github.com/jingyig16/healthdashboard
"""

# Importing libraries
import dash_bootstrap_components as dbc
from dash import html


def homepage():
    """ Defines the layout for the home page in the dashboard
        with headings, paragraphs, and images.

    :return: The layout for the home page in the dashboard
    """
    # homepage layout with instructions on how to navigate the dashboard
    return dbc.Container([
        html.Br(),
        html.H1("Welcome to Fitbit Insights Dashboard", className="text-center", style={'color': 'white'}),
        html.P("Select a feature from the navigation menu on the top right to begin analyzing your Fitbit data.",
               className="text-center", style={'color': 'white'}),
        dbc.Row([
            html.Br(),
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Analyze Your Sleep Patterns", className="text-center feature-heading",
                        style={'color': 'white'}),
                html.P(
                    "Discover insights into your sleep efficiency, duration, and latency."\
                    "Understand how your sleep quality varies over time and identify areas for improvement.",
                    className="text-center", style={'color': 'white'}),
            ], md=3, className="feature-box"),
            dbc.Col([
                html.H3("Monitor Your Daily Activity", className="text-center feature-heading",
                        style={'color': 'white'}),
                html.P(
                    "Track your daily steps, distance, calories burned, and active minutes."\
                    "Analyze your progress and set goals to stay motivated and achieve a healthier lifestyle.",
                    className="text-center", style={'color': 'white'}),
            ], md=3, className="feature-box"),
            dbc.Col([
                html.H3("Heart Rate Analysis", className="text-center feature-heading", style={'color': 'white'}),
                html.Br(),
                html.P(
                    "Visualize your heart rate data to better understand your cardiovascular health."\
                    "Identify trends and monitor how your heart rate changes over time.",
                    className="text-center", style={'color': 'white'}),
            ], md=3, className="feature-box"),
            dbc.Col([
                html.H3("Correlation Analysis", className="text-center feature-heading", style={'color': 'white'}),
                html.Br(),
                html.P(
                    "Explore the relationships between various health parameters. Identify patterns and correlations"\
                    "to gain insights on how different aspects of your health are interconnected.",
                    className="text-center", style={'color': 'white'}),
            ], md=3, className="feature-box"),
        ]),
        html.Br(),
        html.Img(src="https://i.postimg.cc/y6XfBjhV/fitbit-image.png", alt='fitbit watch picture',
                 style={'height': '20%', 'width': '20%', 'display': 'block', 'margin': 'auto'})
    ], style={'backgroundColor': 'black'})
