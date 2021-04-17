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
from datetime import date

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
FROM olhc AS o;"""

curs.execute(testy)

data = []
for x in curs:
    data.append(x)

df = pd.DataFrame(data, columns=['ticker', 'issuer', 'session_date', 'open', 'close', 'min'])

# convert the 'Session_date' column to datetime format
df['session_date'] = pd.to_datetime(df['session_date'])

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
        dcc.DatePickerRange(
            id='my-date-picker-range',
            calendar_orientation='horizontal',
            day_size=30,
            first_day_of_week=1,  # 0 Sunday
            clearable=False,
            with_portal=False,  # True on the page
            min_date_allowed=date(2010, 1, 1),
            max_date_allowed=date(2021, 12, 31),
            initial_visible_month=date(2018, 1, 1),
            start_date=date(2018, 1, 1),
            end_date=date(2021, 12, 31),
            display_format='MMM Do, YYYY',  # lots possibilities

            updatemode='singledate'
        ),
        html.Div(id='output-container-date-picker-range'),

        # -----------------------------------
        # Define Dropdown
        # -----------------------------------

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
# -----------------------------------

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback(
    Output('indicators', 'figure'),
    [Input('issuer_selection', 'value'),
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')
     ])
def retrieve_plots(issuer, start_date, end_date):
    fil_df = df[df['issuer'] == issuer]
    # Creating trace1
    trace1 = go.Scatter(x=(fil_df[(fil_df['session_date'] > start_date)][fil_df['session_date'] < end_date]["session_date"]),
                        y=fil_df['close'],
                        mode="markers",
                        name="Close price",
                        marker=dict(color='#21617A', size=4),
                        text=fil_df['session_date'])

    # Creating trace2
    trace2 = go.Scatter(x=(fil_df[(fil_df['session_date'] > start_date)][fil_df['session_date'] < end_date]["session_date"]),
                        y=fil_df['open'],
                        mode="markers",
                        name="Open price",
                        marker=dict(color='#C22E4C', size=3),
                        text=fil_df['session_date'])

    # Creating trace3
    trace3 = go.Scatter(x=(fil_df[(fil_df['session_date'] > start_date)][fil_df['session_date'] < end_date]["session_date"]),
                        y=fil_df['min'],
                        mode="markers",
                        name="Min price",
                        marker=dict(color='#7FD13A', size=2),
                        text=fil_df['session_date'])

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
