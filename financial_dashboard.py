# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from mysql.connector import Error
import mysql.connector
import pandas as pd

# -----------------------------------
# Connect to database OR data source here
# -----------------------------------

try:
    db = mysql.connector.connect(
        user="fellow",
        password="fellow2021",
        host="51.83.129.54",
        port=3306,
        database="fellowshippl"
    )

except Error as e:
    print("Error while connecting to MySQL", e)
    quit()

# -----------------------------------
# Retrieve data from database
# -----------------------------------

curs = db.cursor()

testy = """SELECT fc.ticker, c.issuer, fc.indicator, fc.year, fc.quarter, fc.value 
FROM financial_calculated_data AS fc
INNER JOIN companies AS c
ON c.ticker = fc.ticker """

curs.execute(testy)

data = []
for x in curs:
    data.append(x)

df = pd.DataFrame(data, columns=['ticker', 'issuer', 'indicator', 'year', 'quarter', 'value'])
print(df.sample())

# df.info()
# print(round(df.describe(), 2))

# -----------------------------------
# Initialize the app
# This application is using a custom
# CSS stylesheet to modify the default
# styles of the elements.
# -----------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = dict(background='#ffff',
              text='#36017A',
              font='#C2BF4E')

# -----------------------------------
# Define app layout
# -----------------------------------

app.layout = html.Div(children=[
    html.H1(children='Financial Dashboard for FellowshipPL',
            style={'textAlign': 'center', 'color': colors['text']}
            ),
    html.Div(children=[
        html.Div(style={
            'textAlign': 'center', 'color': colors['font']
            },
            children='''Financial Project Web Application
        '''),

# -----------------------------------
# Define Dropdown
# By #ticker or by name
# -----------------------------------

        # dcc.Dropdown(style={
        #     'textAlign': 'left',
        #     'color': colors['text']
        #
        # },
        #     id='ticker_selection',
        #     options=[
        #         {'label': i, 'value': i} for i in df.ticker.unique()
        #     ], multi=False,
        #     placeholder='Filter by ticker of company ...'),
        # html.H3(id='text'),
        # dcc.Graph(id='indicators')])
        #     ])

        dcc.Dropdown(style={
                    'textAlign': 'left',
                    'color': colors['text']

                },
                    id='issuer_selection',
                    options=[
                        {'label': i, 'value': i} for i in df.issuer.unique()
                    ], multi=False,
                    placeholder='Filter by name of company ...'),
                html.H3(id='text'),
                dcc.Graph(id='indicators')])
                    ])

# -----------------------------------
# Define callback
# By #ticker or by name
# -----------------------------------

# @app.callback(Output('indicators', 'figure'),
#               [Input('ticker_selection', 'value')])
# def retrieve_plots(ticker):
#     filtered_df = df[df['ticker'] == ticker]

@app.callback(Output('indicators', 'figure'),
              [Input('issuer_selection', 'value')])
def retrieve_plots(issuer):
    filtered_df = df[df['issuer'] == issuer]

    # Creating trace1
    trace1 = go.Scatter(x=filtered_df['year'],
                        y=filtered_df[filtered_df['indicator'] == 'ROA']['value'],
                        mode="lines+markers",
                        name="Indicator ROA",
                        marker=dict(color='#B780FF'),
                        text=filtered_df.year)

    # Creating trace2
    trace2 = go.Scatter(x=filtered_df['year'],
                        y=filtered_df[filtered_df['indicator'] == 'WBP']['value'],
                        mode="lines+markers",
                        name="Indicator WBP",
                        marker=dict(color='#C2BF4E'),
                        text=filtered_df.year)

    # Creating trace3
    trace3 = go.Scatter(x=filtered_df['year'],
                        y=filtered_df[filtered_df['indicator'] == 'tsk']['value'],
                        mode="markers+lines",
                        name="Indicator tsk",
                        marker=dict(color='#36017A'),
                        text=filtered_df.year)


    data = [trace1, trace2, trace3]

    layout = dict(yaxis=dict(title='Prices', ticklen=5, zeroline=False),
                  xaxis=dict(title='Date', ticklen=5, zeroline=False),
                  hovermode="x unified",
                  style={'textAlign': 'center',
                         'color': colors['text']
                         },
                  )
    datapoints = {'data': data, 'layout': layout}
    return datapoints

# -----------------------------------
# Run the app
# -----------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
