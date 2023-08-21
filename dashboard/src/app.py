import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html
from pinotdb import connect

from settings.settings import settings

conn = connect(host=settings.PINOT_HOST, port=settings.PINOT_PORT)
curs = conn.cursor()

app = Dash(__name__, title="Order Delivery Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

"""
Select the metrics for the last 2 minutes
"""


def get_metrics():
    query = """
    select count(*) FILTER(WHERE  ts > ago('PT1M')) AS events1Min,
           count(*) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS events1Min2Min,
           sum(total_price) FILTER(WHERE  ts > ago('PT1M')) AS total1Min,
           sum(total_price) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS total1Min2Min
    from orders 
    where ts > ago('PT2M')
    limit 1
    """
    curs.execute(query)
    df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
    average_order_value_1min = df['total1Min'].values[0] / int(df['events1Min'].values[0])
    return dbc.Row([
            dbc.Col(html.Div(children=[
                html.H3(children='# of Orders'),
                html.H1(children=int(df['events1Min'].values[0]))
            ])),
            dbc.Col(html.Div(children=[
                html.H3(children='Revenue in $'),
                html.H1(children=df['total1Min'].values[0])
            ])),
            dbc.Col(html.Div(children=[
                html.H3(children='Average order value in $'),
                html.H1(children=average_order_value_1min)
            ])),
        ])


"""
Select the latest 10 orders
"""
def get_latest_orders():
    query = """
    SELECT ToDateTime(ts, 'HH:mm:ss:SSS') AS dateTime, total_price, user_id, products_ordered, total_quantity
    FROM orders
    ORDER BY ts DESC
    LIMIT 10
    """
    curs.execute(query)
    df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
    return html.Div(children=[
        html.H3(children='Latest Order', style={'textAlign': 'center'}),
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    ])


"""
Create the layout
"""
app.layout = dbc.Container([
    html.H1(children='Order Delivery Analytics', style={'textAlign': 'center'}),
    get_metrics(),
    html.Br(),
    get_latest_orders()
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
