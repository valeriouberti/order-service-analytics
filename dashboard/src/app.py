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

Get graph of orders per hour
"""


def get_graphs():
    query = """
    select ToDateTime(DATETRUNC('minute', ts), 'yyyy-MM-dd HH:mm:ss') AS dateMin, 
    count(*) AS orders, 
    sum(total_price) AS revenue
    from orders 
    where ts > ago('PT1H')
    group by dateMin
    order by dateMin desc
    LIMIT 10000
    """
    curs.execute(query)
    df_ts = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
    df_ts_melt = pd.melt(df_ts, id_vars=['dateMin'], value_vars=['revenue', 'orders'])
    orders = df_ts_melt[df_ts_melt.variable == "orders"]
    latest_date = orders.dateMin.max()

    revenue_complete = orders[orders.dateMin < latest_date]
    fig = go.Figure(data=[
        go.Scatter(x=revenue_complete.dateMin,
                   y=revenue_complete.value, mode='lines',
                   line={'dash': 'solid', 'color': 'green'}),
    ])
    fig.update_layout(showlegend=False, title="Orders per minute",
                      margin=dict(l=0, r=0, t=40, b=0), )
    fig.update_yaxes(range=[0, df_ts["orders"].max() * 1.1])

    return fig


"""
Create the layout
"""
app.layout = dbc.Container([
    html.H1(children='Order Delivery Analytics', style={'textAlign': 'center'}),
    html.Div(id='live-update-metrics'),
    html.Div([
        dcc.Graph(figure=get_graphs()),
    ]
    ),
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
