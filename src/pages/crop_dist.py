from dash import Dash, html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sidebar import sidebar
from navbar import navbar


register_page(__name__, path='/visualize/crop-distribution')

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
                            id='commodity',
                            options=[{'label': commodity, 'value': commodity}
                                     for commodity in data['commodity'].unique()],
                            value=[
                                commodity for commodity in data['commodity'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='commodity-pie',
                                  style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='crop-box',
                            options=[{'label': crop, 'value': crop}
                                     for crop in data['commodity'].unique()],
                            value=[crop for crop in data['commodity'].unique()],
                            multi=True
                        ),
                        dcc.Graph(id='box-crop', style={'height': '540px'}),
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
    Output('commodity-pie', 'figure'),
    [Input('commodity', 'value')]
)
def commodity_pie(value):
    df = data[data['commodity'].isin(value)]
    fig = px.pie(df, names='commodity', title='Commodity Distribution')
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.03, 0.03, 0.03],
        marker=dict(line=dict(color='black', width=2))
    )
    fig.update_layout(
        margin=dict(t=40, b=30),
        title_x=0.5
    )
    return fig

@callback(
    Output('box-crop', 'figure'),
    [Input('crop-box', 'value')]
)
def box_dist(value):
    df = data[data['commodity'].isin(value)]
    fig = px.box(df, x='commodity', y='price', title='Price Distribution by Commodity', labels={
                 'commodity': 'Commodity', 'price': 'Price'})
    fig.update_layout(
        margin=dict(l=40, r=40, t=50, b=30),
        title_x=0.5,
        title_y=0.96
    )
    return fig