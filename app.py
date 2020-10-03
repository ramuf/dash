import os
from random import randint

import plotly.plotly as py
from plotly.graph_objs import *

import flask
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)


# Put your Dash code here
df = pd.read_csv("covid-19-allegheny.csv")

fig_total_cases = px.line(df, x=df.date, y=df.cases, title='Total Cases')

app.layout = html.Div([

    html.H1("Allegheny County COVID-19 Dashboard", style={'text-align': 'center'}),
    dcc.Graph(id='my_bee_map', figure=fig_total_cases),
    # dcc.Graph(id='my_bee_map2', figure={}),
    # dcc.Graph(id='my_bee_map3', figure={})

])

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
    
