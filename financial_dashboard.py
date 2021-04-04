import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from mysql.connector import Error
import mysql.connector

# -----------------------------------
# Initialize the app
# -----------------------------------


app = dash.Dash(__name__)

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

testy = """SELECT ticker, indicator, year, quarter, value
FROM financial_calculated_data fcd """

curs.execute(testy)

data = []
for x in curs:
    data.append(x)

df = pd.DataFrame(data, columns=['ticker', 'indicator', 'year', 'quarter', 'value'])
df.sample(20)

df.info()
print(round(df.describe(), 2))

# -----------------------------------
# Define app layout
# -----------------------------------

app.layout = html.Div([
    html.H1('Financial Dashboard'),
    html.Div([
        dcc.Dropdown(
            id='ticker_selection',
            options=[
                {'label': i, 'value': i} for i in df.ticker.unique()
            ], multi=False, placeholder='Filter by ticker...'),
        html.H3(id='text'),
        dcc.Graph(id='indicators')])
])

app.title = 'Financial Dashboard'



# -----------------------------------
# Define callback
# -----------------------------------

@app.callback(Output('indicators', 'figure'),
              [Input('ticker_selection', 'value')])
def retrieve_plots(ticker):
    filtered_df = df[df['ticker'] == ticker]
    trace1 = go.Scatter(x=filtered_df['year'],
                        y=filtered_df[filtered_df['indicator'] == 'WSP']['value'],
                        mode="markers",
                        name="Indicator WSP",
                        marker=dict(color='red'),
                        text=filtered_df.year)

    # Creating trace2
    trace2 = go.Scatter(x=filtered_df['year'],
                        y=filtered_df[filtered_df['indicator'] == 'ROA']['value'],
                        mode="lines",
                        name="Indicator ROA",
                        marker=dict(color='blue'),
                        text=filtered_df.year)

    # Creating trace3
    trace3 = go.Scatter(x=filtered_df['year'],
                        y=filtered_df[filtered_df['indicator'] == 'wog']['value'],
                        mode="lines+markers",
                        name="Indicator wog",
                        marker=dict(color='green'),
                        text=filtered_df.year)

    data = [trace1, trace2, trace3]

    layout = dict(title='Wykresy predykcji cen akcji',
                  xaxis=dict(title='Czas w latach', ticklen=5, zeroline=False),
                  hovermode="x unified")
    datapoints = {'data': data, 'layout': layout}
    return datapoints


@app.callback(Output(component_id='text', component_property='children'),
              [Input(component_id='ticker_selection', component_property='value')])
def update_output_div(ticker_value):
    return 'Displaying data for company with ticker "{}"'.format(ticker_value)


# -----------------------------------
# Run the app
# -----------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
