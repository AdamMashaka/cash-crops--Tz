from dash import html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sidebar import sidebar
from navbar import navbar


register_page(__name__, path='/visualize/high-low-prices')

data = pd.read_csv('../Data/needed_food_data.csv')


layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    html.Div(children=[
        sidebar,

        html.Div(
            style={'paddingTop': '95px', 'paddingLeft': '230px',
                   'paddingRight': '30px', 'display': 'grid', 'gap': '25px', 'height': 'calc(100vh - 130px)'},

            children=[
                html.Div([
                    dbc.RadioItems(
                        id="high-low-radios",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Market", "value": "market"},
                            {"label": "Monthly", "value": "month"},
                            {"label": "Yearly", "value": "year"},
                        ],
                        value="market",
                        style={"float": "right"}
                    ),
                ]),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='high-low-graph',
                                  style={'height': '540px'}),
                    ])
                ],
                style={'boxShadow': '0px 1px 5px #999', 'marginBottom': '25px'})

            ]),
    ])
])



# callback

@callback(
    Output('high-low-graph', 'figure'),
    Input('high-low-radios', 'value')
)
def update_high_low_graph(value):
    max_prices = data.groupby(value)["price"].max().reset_index()
    min_prices = data.groupby(value)["price"].min().reset_index()

    fig = px.scatter(max_prices, x=value, y="price", color_discrete_sequence=["green"], 
                    labels={"price": "Max Price", "year":"Year", "month":"Month", "market":"Market"}, title=f"Highest and Lowest Prices by {value.capitalize()}")
    fig.add_trace(px.scatter(min_prices, x=value, y="price", color_discrete_sequence=["red"], 
                            labels={"price": "Min Price", "year":"Year", "month":"Month", "market":"Market"}).data[0])

    for year, max_price in zip(max_prices[value], max_prices['price']):
        fig.add_shape(type="line",
                    x0=year, x1=year, y0=0, y1=max_price,
                    line=dict(color="green", width=2))

    for year, min_price in zip(min_prices[value], min_prices['price']):
        fig.add_shape(type="line",
                    x0=year, x1=year, y0=0, y1=min_price,
                    line=dict(color="red", width=2))
        
    fig.update_traces(marker=dict(size=12, symbol="circle"),
                    selector=dict(mode='markers'))

    fig.update_layout(legend=dict(traceorder='reversed'), yaxis=dict(title='Price'), title_x=0.5, xaxis_tickangle=-45)

    return fig