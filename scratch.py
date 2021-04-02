import pandas as pd

import plotly.offline as pyo
import plotly.graph_objs as go

df1 = pd.read_csv('/Users/dorotagawronska-popa/Documents/finances/df_wsk_rent_concat.csv', index_col = 0)
print(df1)

tickers = ['KGH', 'AMC', '06N', 'ZWC', 'PLZ', 'EST', 'MON', 'SFG', 'RPC', 'NTT', 'PHR']

data = []

for ticker in tickers:
    trace = go.Scatter(x=df1['period'],
                       y=df1[df1['ticker'] == ticker]['ROS'],
                       mode='lines', name=ticker)
    data.append(trace)

# Define the Layout
layout = go.Layout(title='Wskaźniki rentowności')

# Greate figure and plot the figure
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig)
