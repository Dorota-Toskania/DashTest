import dash
import pandas as pd

import plotly.offline as pyo
import plotly.graph_objs as go
# import plotly.express as px
# from plotly.offline import init_notebook_mode, iplot, plot

import dash_core_components as dcc
import dash_html_components as html

# Initialize the app
app = dash.Dash(__name__)

# Connect to database OR data source here

import mysql.connector

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

# pobieram dane z bazy

curs = db.cursor()

testy = """SELECT ticker, indicator, year, quarter, value
FROM financial_calculated_data fcd """

curs.execute(testy)

data = []
for x in curs:
    data.append(x)

df = pd.DataFrame(data, columns=['ticker', 'indicator', 'year', 'quarter', 'value'])
df.sample(20)

df.info()
print(round(df.describe(),2))

# Define graphs

# Creating trace1
trace1 = go.Scatter(x = df['year'],
                    y = df[df['indicator']=='WSP']['value'],
                    mode = "markers",
                    name = "Indicator WSP",
                    marker = dict(color = 'red'),
                    text= df.year)

# Creating trace2
trace2 = go.Scatter(x = df['year'],
                    y = df[df['indicator']=='ROA']['value'],
                    mode = "lines",
                    name = "Indicator ROA",
                    marker = dict(color = 'blue'),
                    text= df.year)

# Creating trace3
trace3 = go.Scatter(x = df['year'],
                    y = df[df['indicator']=='wog']['value'],
                    mode = "lines+markers",
                    name = "Indicator wog",
                    marker = dict(color = 'green'),
                    text= df.year)

dcc.Dropdown(
    options=[
        {'label': '06N', 'value': '06N'},
        {'label': 'KGH', 'value': 'KGHM'},
        {'label': 'ZWC', 'value': 'ZWC'}
    ],
    value='MTL'
)

data = [trace1, trace2, trace3]
layout = dict(title = 'Wykresy predykcji cen akcji',
              xaxis= dict(title= 'Czas w latach',ticklen= 5,zeroline= False),
              hovermode="x unified")
fig = dict(data = data, layout = layout)

# plotowanie w notebook (iplot(fig))

# plot webowy w przeglądarce
pyo.plot(fig)

# Define the app Layout
app.title = 'My first own Dashboard'
app.layout = html.Div()

# Define callback

# Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)


