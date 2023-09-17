from dash import html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
from sidebar import sidebar
import plotly.express as px
from navbar import navbar


register_page(__name__, path='/visualize/market-volume')

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
                            id='market',
                            options=[{'label': market, 'value': market}
                                     for market in data['market'].unique()],
                            value=[market for market in data['market'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='market-data', style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='market-commodity',
                            options=[{'label': market, 'value': market}
                                     for market in data['market'].unique()],
                            value=[market for market in data['market'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='market-bar', style={'height': '540px'}),
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
    Output('market-data', 'figure'),
    [Input('market', 'value')]
)
def update_market(value):
    df = data[data['market'].isin(value)]
    fig = px.histogram(df, x='market')
    fig.update_layout(
        yaxis=dict(title='Count (x100KG)'),
        xaxis=dict(title='Market'),
        xaxis_tickangle=-30,
        margin=dict(l=40, r=40, t=50, b=40),
        title='Markets Volume',
        title_x=0.5,
        title_y=0.96
    )
    return fig

@callback(
    Output('market-bar', 'figure'),
    [Input('market-commodity', 'value')]
)
def market_bar(value):
    df = data[data['market'].isin(value)]
    grouping = df.groupby('market')['commodity'].value_counts().unstack()
    fig = px.bar(grouping, x=grouping.index, y=grouping.columns,
                 title='Commodity Counts by Market', labels={'y': 'Count', 'index': 'Market'})
    fig.update_layout(
        yaxis=dict(title='Value'),
        xaxis=dict(title='Market'),
        xaxis_tickangle=-30,
        margin=dict(l=40, r=40, t=50, b=30),
        title_x=0.5,
        legend_title='Commodity',
        title_y=0.96
    )
    return fig
