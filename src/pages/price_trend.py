from dash import Dash, html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sidebar import sidebar
from navbar import navbar


register_page(__name__, path='/visualize/price-trend')

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
                            id='crops',
                            options=[{'label': crop, 'value': crop}
                                     for crop in data['commodity'].unique()],
                            value=[crop for crop in data['commodity'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='crops-data', style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='year',
                            options=[{'label': year, 'value': year}
                                     for year in data['year'].unique()],
                            value=[year for year in data['year'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='price-trend', style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='month',
                            options=[{'label': month, 'value': month}
                                     for month in data['month'].unique()],
                            value=[month for month in data['month'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='month-price-trend',
                                  style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='crops-month',
                            options=[{'label': crop, 'value': crop}
                                     for crop in data['commodity'].unique()],
                            value=[crop for crop in data['commodity'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='crops-month-data',
                                  style={'height': '540px'}),
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
    Output('crops-data', 'figure'),
    [Input('crops', 'value')]
)
def update_graph(value):
    average_prices = data.groupby(['year', 'commodity'])[
        'price'].mean().reset_index()
    df = average_prices[average_prices['commodity'].isin(value)]
    fig = px.line(df, x='year', y='price',
                  color='commodity', markers='line+markers')
    fig.update_layout(
        xaxis=dict(title='Year'),
        yaxis=dict(title='Average Price'),
        xaxis_tickangle=-45,
        margin=dict(l=40, r=40, t=50, b=50),
        title=f'Average Price Trends for {" , ".join(value)}',
        title_x=0.5,
        title_y=0.96,
    )
    return fig


@callback(
    Output('price-trend', 'figure'),
    [Input('year', 'value')]
)
def price_trend(value):
    df = data[data['year'].isin(value)]
    year_commodity_avg = df.groupby(['year', 'commodity'])[
        'price'].mean().reset_index()
    fig = px.bar(
        year_commodity_avg,
        x='year', y='price',
        color='commodity',
        title='Average Price of Commodities Over the Years', labels={'year': 'Year', 'price': 'Average Price'},
        barmode='group'
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=30),
        legend_title='Commodity',
        title_x=0.5,
        title_y=0.96
    )
    return fig


@callback(
    Output('month-price-trend', 'figure'),
    [Input('month', 'value')]
)
def price_trend(value):
    df = data[data['month'].isin(value)]
    month_commodity_avg = df.groupby(['month', 'commodity'])[
        'price'].mean().reset_index()
    fig = px.bar(
        month_commodity_avg,
        x='month', y='price',
        color='commodity',
        title='Average Price of Commodities Over the Months', labels={'month': 'Month', 'price': 'Average Price'},
        barmode='group'
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=30),
        legend_title='Commodity',
        title_x=0.5,
        title_y=0.96
    )
    return fig

@callback(
    Output('crops-month-data', 'figure'),
    [Input('crops-month', 'value')]
)
def update_graph(value):
    average_prices = data.groupby(['month', 'commodity'])[
        'price'].mean().reset_index()
    df = average_prices[average_prices['commodity'].isin(value)]
    fig = px.line(df, x='month', y='price',
                  color='commodity', markers='line+markers')
    fig.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='Average Price'),
        xaxis_tickangle=-45,
        margin=dict(l=40, r=40, t=50, b=30),
        title=f'Average Price Trends for {" , ".join(value)}',
        title_x=0.5,
        title_y=0.96
    )
    return fig