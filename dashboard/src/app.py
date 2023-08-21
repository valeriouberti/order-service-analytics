import pandas as pd
from dash import Dash, html
from pinotdb import connect

app = Dash(__name__, title="dashboard")


def total_price(df):
    return df['total_price'].sum()


conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()

curs.execute("""select * from orders limit 10""")
df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    html.Div(children=[
        html.H2('TOTAL PRICE'),
        html.P(id='total-price', children=total_price(df)),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
