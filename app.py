import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.io as pio

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import *
pio.templates.default = "seaborn"

app = dash.Dash(__name__)
app.title = 'COVID-19 Allegheny Dashboard'

server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/FranklinChen/covid-19-allegheny-county/master/covid-19-allegheny-county.csv')
# df = pd.read_csv('https://raw.githubusercontent.com/ramuf/covid-19-data-1/master/us-counties.csv')
# df = df[(df['county'] == 'Allegheny') & (df['state'] == 'Pennsylvania')]
df['population'] = 1216045
df['new_cases'] = df.cases.diff()
df['new_deaths'] = df.deaths.diff()
df['new_cases_smoothed'] = round(df.new_cases.rolling(min_periods=7, window=7).mean(), 1)
df['deaths_poll'] = round(df.deaths/df.population*100000, 1)
df['cases_fatality'] = round(df.deaths/df.cases*100, 1)
df['daily_incidence'] = round(df.new_cases/df.population*100000, 1)
df['seven_days_incidence'] = round(df.new_cases.rolling(min_periods=7, window=7).sum()/df.population*100000, 1)

last_date = df.date.max()
new_cases = df.new_cases.tail(1)
total_cases = df.cases.tail(1)
total_deaths = df.deaths.tail(1)
fatality = df.cases_fatality.tail(1)
incidence = df.daily_incidence.tail(1)
seven_day_incidence = df.seven_days_incidence.tail(1)

grid_color = '#7f7f7f'
line_color = '#e95846'

layout = Layout(
    paper_bgcolor='#403e3d',
    plot_bgcolor='#403e3d',
    font_color="white",
    margin=dict(pad=10),
    # colorway=['red'],
    # hovermode='x',
    hoverlabel = dict(
        bgcolor="#403e3d",
        # font_size=16,
        # font_family="Rockwell"
    )
)

fig_new_cases_absolute = px.line(df, x='date', y='new_cases', labels={'date':'Date', 'new_cases':'New Cases'}, title='New Cases (Absolute)').update_layout(layout)
fig_new_cases_absolute.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_absolute.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_absolute.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>New Cases: %{y}')

fig_new_deaths = px.line(df, x='date', y='new_deaths', labels={'date':'Date', 'new_deaths':'New Deaths'}, title='New Deaths').update_layout(layout)
fig_new_deaths.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_deaths.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_deaths.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>New Deaths: %{y}')

fig_total_cases = px.line(df, x='date', y='cases', labels={'date':'Date', 'cases':'Total Cases'}, title='Total Cases').update_layout(layout)
fig_total_cases.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_total_cases.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_total_cases.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>Total Cases: %{y}')

fig_total_deaths = px.line(df, x='date', y='deaths', labels={'date':'Date', 'deaths':'Total Deaths'}, title='Total Deaths').update_layout(layout)
fig_total_deaths.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_total_deaths.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_total_deaths.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>Total Deaths: %{y}')

fig_fatality = px.line(df, x='date', y='cases_fatality', labels={'date':'Date', 'cases_fatality':'Fatality %'}, title='Fatality % (Total Deaths divided by Total Cases)').update_layout(layout)
fig_fatality.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_fatality.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_fatality.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>Fatality: %{y}%')

fig_deaths_poll = px.line(df, x='date', y='deaths_poll', labels={'date':'Date', 'deaths_poll':'Deaths per 100k'}, title='Deaths per 100k population').update_layout(layout)
fig_deaths_poll.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_deaths_poll.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_deaths_poll.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>Deaths per 100k: %{y}')

fig_new_cases_smoothed = px.line(df, x='date', y='new_cases_smoothed', labels={'date':'Date', 'new_cases_smoothed':'New Cases Smoothed'}, title='New Cases Smoothed (7 Days average)').update_layout(layout)
fig_new_cases_smoothed.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_smoothed.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_smoothed.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>New Cases Smoothed: %{y}')

fig_new_cases_incidence = px.line(df, x='date', y='daily_incidence', labels={'date':'Date', 'daily_incidence':'Daily Incidence Rate'}, title='Daily Incidence Rate (per 100K population)').update_layout(layout)
fig_new_cases_incidence.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_incidence.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_incidence.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>Daily Incidence Rate: %{y}')

fig_new_cases_incidence_7_days = px.line(df, x='date', y='seven_days_incidence', labels={'date':'Date', 'seven_days_incidence':'Seven Day Incidence Rate'}, title='7 Days New Cases Incidence (New Cases per 100K population for the past 7 days)').update_layout(layout)
fig_new_cases_incidence_7_days.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_incidence_7_days.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color)
fig_new_cases_incidence_7_days.update_traces(line_color=line_color, hovertemplate='%{x} <br><br>Seven Day Incidence Rate: %{y}')

app.layout = html.Div([
    # html.Br(),

    # html.H1("Allegheny County COVID-19 Dashboard", style={'text-align': 'center', 'background-color': 'lightblue'}),
    html.H1("Allegheny County COVID-19 Dashboard", className='title'),

    # html.Br(),

    html.Div(className='totals', children=[
        html.Div(className= 'pricing-table', children=[
            html.H3('Last Update', className='pricing-title'),
            html.Div(children=last_date, className='price')
        ]),
        html.Div(className='pricing-table', children=[
            html.H3('New Cases', className='pricing-title'),
            html.Div(children=new_cases, className='price')
        ]),
        html.Div(className='pricing-table', children=[
            html.H3('Total Cases', className='pricing-title'),
            html.Div(children=total_cases, className='price')
        ]),
        html.Div(className='pricing-table', children=[
            html.H3('Total Deaths', className='pricing-title'),
            html.Div(children=total_deaths, className='price')
        ]),
        html.Div(className='pricing-table', children=[
            html.H3('Fatality %', className='pricing-title'),
            html.Div(children=fatality, className='price')
        ]),
        html.Div(className='pricing-table', children=[
            html.H3('Daily Incidence Rate *', className='pricing-title'),
            html.Div(children=incidence, className='price')
        ]),
        html.Div(className='pricing-table', children=[
            html.H3('7 Day Incidence Rate **', className='pricing-title'),
            html.Div(children=seven_day_incidence, className='price')
        ]),
    ]),

    html.Br(),

    # html.Div(className='graphs_top', children=[
    #     html.Div(children=[
    #         dcc.Graph(id='new_cases_absolute', figure=fig_new_cases_absolute),
    #         dcc.Graph(id='new_deaths', figure=fig_new_deaths),
    #     ]),
    # ]),
    html.Div(className='graphs_top', children=[
        dcc.Graph(id='new_cases_absolute', figure=fig_new_cases_absolute),
        dcc.Graph(id='new_deaths', figure=fig_new_deaths),
    ]),
    html.Br(),

    html.Div(children=[
        html.Div(className='graphs_bottom', children=[
            dcc.Graph(id='total_cases', figure=fig_total_cases),
            dcc.Graph(id='total_deaths', figure=fig_total_deaths),
            dcc.Graph(id='fatality', figure=fig_fatality),
        ]),

        html.Br(),

        html.Div(className='graphs_bottom', children=[
            dcc.Graph(id='deaths_poll', figure=fig_deaths_poll),
            dcc.Graph(id='new_cases_smoothed', figure=fig_new_cases_smoothed),
            dcc.Graph(id='new_cases_incidence', figure=fig_new_cases_incidence)
        ])
    ]),

    # html.Div(className='graphs',children=[dcc.Graph(id='new_cases_absolute_', figure=fig_new_cases_absolute)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='new_deaths_', figure=fig_new_deaths)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='total_cases_', figure=fig_total_cases)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='total_deaths_', figure=fig_total_deaths)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='fatality_', figure=fig_fatality)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='deaths_poll_', figure=fig_deaths_poll)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='new_cases_smoothed_', figure=fig_new_cases_smoothed)]),
    # html.Div(className='graphs',children=[dcc.Graph(id='new_cases_incidence_', figure=fig_new_cases_incidence)]),


    html.Br(),
    html.H2('* Daily Incidence Rate: Number of new cases per 100k residents', style={'margin' : '10px'}),
    html.Br(),
    html.H2('** 7 Day Incidence Rate: Sum of the past 7 daily incidence rates', style={'margin' : '10px'}),
    html.Br(),
    html.Div([
        html.A('Dashboard generated from Franklin Chen dataset',
               href='https://github.com/FranklinChen/covid-19-allegheny-county',
               target="_blank",
               style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold', 'font-size': 15, 'margin' : '10px'}),
        # dcc.Link('Dashboard generated from Franklin Chen dataset',
        #          href='https://github.com/FranklinChen/covid-19-allegheny-county',
        #          style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold', 'font-size': 14, 'color' : 'grey'})
    ]),
    # html.Link('Dashboard generated from Franklin Chen dataset', href='https://github.com/FranklinChen/covid-19-allegheny-county'),
    html.Br(),
    html.Br(),
])

if __name__ == '__main__':
    app.run_server(debug=True)
