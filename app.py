import pandas as pd
import plotly.express as px  # (version 4.7.0)
# import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/FranklinChen/covid-19-allegheny-county/master/covid-19-allegheny-county.csv')

df['population'] = 1216045
df['new_cases'] = df.cases.diff()
df['new_deaths'] = df.deaths.diff()
df['new_cases_smoothed'] = round(df.new_cases.rolling(min_periods=7, window=7).mean(), 1)
df['deaths_poll'] = round(df.deaths/df.population*100000, 1)
df['cases_fatality'] = round(df.deaths/df.cases*100, 1)
df['daily_incidence'] = round(df.new_cases/df.population*100000, 1)
df['7_days_incidence'] = round(df.new_cases.rolling(min_periods=7, window=7).sum()/df.population*100000, 1)

fig_total_cases = px.line(df, x=df.date, y=df.cases, title='Total Cases').update_layout(margin=dict(pad=10))
fig_new_cases_absolute = px.line(df, x=df.date, y=df.new_cases, title='New Cases (Absolute)').update_layout(margin=dict(pad=10))
fig_new_cases_smoothed = px.line(df, x=df.date, y=df.new_cases_smoothed, title='New Cases Smoothed (7 Days average)').update_layout(margin=dict(pad=10))
fig_new_cases_incidence = px.line(df, x=df.date, y=df.daily_incidence, title='New Cases Incidence (per 100K population)').update_layout(margin=dict(pad=10))
fig_new_cases_incidence_7_days = px.line(df, x=df.date, y=df['7_days_incidence'], title='7 Days New Cases Incidence (New Cases per 100K population for the past 7 days)').update_layout(margin=dict(pad=10))
fig_total_deaths = px.line(df, x=df.date, y=df.deaths, title='Total Deaths').update_layout(margin=dict(pad=10))
fig_new_deaths = px.line(df, x=df.date, y=df.new_deaths, title='New Deaths').update_layout(margin=dict(pad=10))
fig_deaths_poll = px.line(df, x=df.date, y=df.deaths_poll, title='Deaths per 100k population').update_layout(margin=dict(pad=10))
fig_fatality = px.line(df, x=df.date, y=df.cases_fatality, title='Fatality % (Total Deaths divided by Total Cases)').update_layout(margin=dict(pad=10))

figures = ['fig_total_cases', 'fig_new_cases_absolute', 'fig_new_cases_smoothed', 'fig_new_cases_incidence',
           'fig_new_cases_incidence_7_days', 'fig_total_deaths', 'fig_new_deaths', 'fig_deaths_poll', 'fig_deaths_poll']

# for fig in figures:
#     fig.update_layout(margin=dict(pad=10))

app.layout = html.Div([

    html.H1("Allegheny County COVID-19 Dashboard", style={'text-align': 'center'}),

    html.Div([
        dcc.Graph(id='new_cases_absolute', figure=fig_new_cases_absolute),
        dcc.Graph(id='new_deaths', figure=fig_new_deaths),
    ], style={'columnCount': 2}),

    html.Div([
        dcc.Graph(id='total_cases', figure=fig_total_cases),
        dcc.Graph(id='deaths_poll', figure=fig_deaths_poll),

        dcc.Graph(id='total_deaths', figure=fig_total_deaths),
        dcc.Graph(id='new_cases_smoothed', figure=fig_new_cases_smoothed),

        dcc.Graph(id='fatality', figure=fig_fatality),
        # dcc.Graph(id='new_cases_incidence_7_days', figure=fig_new_cases_incidence_7_days),
        dcc.Graph(id='new_cases_incidence', figure=fig_new_cases_incidence),
    ], style={'columnCount': 3})
])

if __name__ == '__main__':
    app.run_server(debug=True)
