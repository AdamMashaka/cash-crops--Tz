from dash import html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sidebar import sidebar
from navbar import navbar


register_page(__name__, path='/visualize/market-price')

data = pd.read_csv('../Data/needed_food_data.csv')


layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    html.Div(children=[
        sidebar,

        html.Div(
            style={'paddingTop': '100px', 'paddingLeft': '230px',
                   'paddingRight': '30px', 'display': 'grid', 'gap': '25px'},

            children=[
                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='market-trend',
                            options=[{'label': market, 'value': market}
                                     for market in data['market'].unique()],
                            value=[market for market in data['market'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='market-price-trend',
                                  style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='market-trend-line',
                            options=[{'label': market, 'value': market}
                                     for market in data['market'].unique()],
                            value=[market for market in data['market'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='market-price-trend-line', style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999', 'marginBottom': '25px'}),

            ]
        )
    ]
    )
]
)


# callbacks

@callback(
    Output('market-price-trend', 'figure'),
    [Input('market-trend', 'value')]
)
def price_trend(value):
    df = data[data['market'].isin(value)]
    market_commodity_avg = data.groupby(['market', 'commodity'])[
        'price'].mean().reset_index()
    fig = px.bar(
        market_commodity_avg,
        x='market', y='price',
        color='commodity',
        title='Average Price of Commodities Over the Markets', labels={'market': 'Market', 'price': 'Average Price'},
        barmode='group'
    )
    fig.update_layout(
        xaxis_tickangle=-30,
        margin=dict(l=40, r=40, t=50, b=30),
        title_x=0.5,
        legend_title='Commodity',
        title_y=0.96
    )
    return fig


@callback(
    Output('market-price-trend-line', 'figure'),
    [Input('market-trend-line', 'value')]
)
def price_trend(value):
    df = data[data['market'].isin(value)]
    market_commodity_avg = data.groupby(['market', 'commodity'])[
        'price'].mean().reset_index()
    fig = px.line(
        market_commodity_avg,
        x='market', y='price',
        color='commodity',
        title='Average Price of Commodities Over the Markets', labels={'market': 'Market', 'price': 'Average Price'},
        markers='line+markers'
    )
    fig.update_layout(
        xaxis_tickangle=-30,
        margin=dict(l=40, r=40, t=50, b=30),
        title_x=0.5,
        legend_title='Commodity',
        title_y=0.96
    )
    return fig
