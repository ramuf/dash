import pandas as pd
import plotly.express as px  # (version 4.7.0)
# import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

server = app.server

df = pd.read_csv("covid-19-allegheny.csv")

fig_total_cases = px.line(df, x=df.date, y=df.cases, title='Total Cases')
fig_new_cases_absolute = px.line(df, x=df.date, y=df.new_cases, title='Total Cases')

app.layout = html.Div([

    html.H1("Allegheny County COVID-19 Dashboard", style={'text-align': 'center'}),
    dcc.Graph(id='total_cases', figure=fig_total_cases),
    dcc.Graph(id='new_cases_absolute', figure=fig_new_cases_absolute),
    # dcc.Graph(id='my_bee_map3', figure={})

])

if __name__ == '__main__':
    app.run_server(debug=True)
