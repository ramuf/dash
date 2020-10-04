import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.io as pio

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

pio.templates.default = "seaborn"

app = dash.Dash(__name__)
app.title = 'COVID-19 Allegheny Dashboard'

server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/FranklinChen/covid-19-allegheny-county/master/covid-19-allegheny-county.csv')

df['population'] = 1216045
df['new_cases'] = df.cases.diff()
df['new_deaths'] = df.deaths.diff()
df['new_cases_smoothed'] = round(df.new_cases.rolling(min_periods=7, window=7).mean(), 1)
df['deaths_poll'] = round(df.deaths/df.population*100000, 1)
df['cases_fatality'] = round(df.deaths/df.cases*100, 1)
df['daily_incidence'] = round(df.new_cases/df.population*100000, 1)
df['seven_days_incidence'] = round(df.new_cases.rolling(min_periods=7, window=7).sum()/df.population*100000, 1)

# layout = dict(margin=dict(pad=10), hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
fig_total_cases = px.line(df, x='date', y='cases', labels={'date':'Date', 'cases':'Total Cases'}, title='Total Cases').update_layout(margin=dict(pad=10))
fig_new_cases_absolute = px.bar(df, x='date', y='new_cases', labels={'date':'Date', 'new_cases':'New Cases'}, title='New Cases (Absolute)').update_layout(margin=dict(pad=10))
fig_new_cases_smoothed = px.line(df, x='date', y='new_cases_smoothed', labels={'date':'Date', 'new_cases_smoothed':'New Cases Smoothed'}, title='New Cases Smoothed (7 Days average)').update_layout(margin=dict(pad=10))
fig_new_cases_incidence = px.line(df, x='date', y='daily_incidence', labels={'date':'Date', 'daily_incidence':'Daily Incidence Rate'}, title='Daily Incidence Rate (per 100K population)').update_layout(margin=dict(pad=10))
fig_new_cases_incidence_7_days = px.line(df, x='date', y='seven_days_incidence', labels={'date':'Date', 'seven_days_incidence':'Seven Day Incidence Rate'}, title='7 Days New Cases Incidence (New Cases per 100K population for the past 7 days)').update_layout(margin=dict(pad=10))
fig_total_deaths = px.line(df, x='date', y='deaths', labels={'date':'Date', 'deaths':'Total Deaths'}, title='Total Deaths').update_layout(margin=dict(pad=10))
fig_new_deaths = px.bar(df, x='date', y='new_deaths', labels={'date':'Date', 'new_deaths':'New Deaths'}, title='New Deaths').update_layout(margin=dict(pad=10))
fig_deaths_poll = px.line(df, x='date', y='deaths_poll', labels={'date':'Date', 'deaths_poll':'Deaths per 100k'}, title='Deaths per 100k population').update_layout(margin=dict(pad=10))
fig_fatality = px.line(df, x='date', y='cases_fatality', labels={'date':'Date', 'cases_fatality':'Fatality %'}, title='Fatality % (Total Deaths divided by Total Cases)').update_layout(margin=dict(pad=10))

last_date = 'Last Update: {}'.format(df.date.max())


app.layout = html.Div([

    html.H1("Allegheny County COVID-19 Dashboard", style={'text-align': 'center', 'background-color': 'lightblue'}),

    html.Br(),

    html.Div([
        html.H4(last_date)
    ]),

    html.Br(),

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
