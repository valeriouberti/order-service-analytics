import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Output, Input, dash_table
from pinotdb import connect

from settings.settings import settings

conn = connect(host=settings.PINOT_HOST, port=settings.PINOT_PORT)
curs = conn.cursor()

app = Dash(__name__, title="Order Delivery Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


"""
Create the layout
"""
app.layout = dbc.Container([
    html.H1(children='Order Delivery Analytics', style={'textAlign': 'center'}),
    html.Div(id='live-update-metrics'),
    html.Br(),
    dbc.Container(children=[
        html.H3(children='Latest Order', style={'textAlign': 'center'}),
        html.Div(id='live-update-orders'),
    ]),
    dcc.Interval(id='interval-component', interval=1 * 1000, n_intervals=0),
], fluid=True)

"""
Select the metrics for the last 2 minutes
"""


@callback(Output('live-update-metrics', 'children'),
          Input('interval-component', 'n_intervals'))
def get_metrics(n):
    query = """
    select count(*) FILTER(WHERE  ts > ago('PT1H')) AS events1Hour,
           sum(total_price) FILTER(WHERE  ts > ago('PT1H')) AS total1Hour
    from orders 
    where ts > ago('PT2H')
    limit 1
    """
    curs.execute(query)
    df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
    average_order_value_1min = df['total1Hour'].values[0] / int(df['events1Hour'].values[0])
    return dbc.Row([
        dbc.Col(html.Div(children=[
            html.H3(children='# of Orders'),
            html.H1(children=int(df['events1Hour'].values[0]))
        ])),
        dbc.Col(html.Div(children=[
            html.H3(children='Revenue in $'),
            html.H1(children=df['total1Hour'].values[0])
        ])),
        dbc.Col(html.Div(children=[
            html.H3(children='Average order value in $'),
            html.H1(children=average_order_value_1min)
        ])),
    ])


@callback(Output('live-update-orders', 'children'),
          Input('interval-component', 'n_intervals'))
def get_latest_orders(n):
    query = """
    SELECT ToDateTime(ts, 'HH:mm:ss:SSS') AS dateTime, total_price, user_id, products_ordered, total_quantity
    FROM orders
    ORDER BY ts DESC
    LIMIT 10
    """
    curs.execute(query)
    df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
    return html.Div([
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ])


if __name__ == '__main__':
    app.run(debug=True, port=8050)
