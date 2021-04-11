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

testy = """SELECT o.ticker, o.issuer, o.session_date, o.open, o.close, o.min
FROM olhc AS o WHERE o.session_date BETWEEN '2019-01-01' AND '2020-12-31'"""

curs.execute(testy)

data = []
for x in curs:
    data.append(x)

df = pd.DataFrame(data, columns=['ticker', 'issuer', 'session_date', 'open', 'close', 'min'])
print(df.sample())

# df.info()
# print(round(df.describe(), 2))

# -----------------------------------
# Initialize the app
# -----------------------------------
# This application is using a custom
# CSS stylesheet to modify the default
# styles of the elements.
# -----------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = dict(background='#3333',
              text='#21617A',
              font='#21617A')

# -----------------------------------
# Define app layout
# -----------------------------------

app.layout = html.Div(children=[
    html.H1(children='Close & Open prices for company',
            style={'textAlign': 'center', 'color': colors['text']}
            ),
    html.Div(children=[
        html.Div(style={
            'textAlign': 'center', 'color': colors['font']
            },
            children='''Financial Dashboard for FellowshipPL
        '''),

# -----------------------------------
# Define Dropdown
# Sample by #ticker or by name
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
# Define first callback
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
    trace1 = go.Scatter(x=filtered_df['session_date'],
                        y=filtered_df['close'],
                        mode="markers",
                        name="Close price",
                        marker=dict(color='#21617A', size=4),
                        text=filtered_df['session_date'])

    # Creating trace2
    trace2 = go.Scatter(x=filtered_df['session_date'],
                        y=filtered_df['open'],
                        mode="markers",
                        name="Open price",
                        marker=dict(color='#C22E4C', size=3),
                        text=filtered_df.session_date)

    # Creating trace3
    trace3 = go.Scatter(x=filtered_df['session_date'],
                        y=filtered_df['min'],
                        mode="markers",
                        name="Min price",
                        marker=dict(color='#7FD13A', size=2),
                        text=filtered_df.session_date)


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