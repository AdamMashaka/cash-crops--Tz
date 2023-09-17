from dash import Dash, html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from navbar import navbar

register_page(__name__, path='/map')

data = pd.read_csv('../Data/needed_food_data.csv')

layout = html.Div([
    navbar,
    html.Div(style={'padding': '70px', 'paddingBottom': '0px', 'paddingTop': '100px'}, children=[
        dbc.Card([
            dcc.Markdown(id='crops'),
            dcc.Graph(
                id='map',
                style={'maxWidth': '100%', 'height': 'calc(100vh - 130px)',
                       'margin': '0', 'padding': '0'},
                config={
                    "scrollZoom": True
                },
            ),
        ], style={'boxShadow': '0px 1px 5px #999'}),
    ])
], style={'overflow': 'hidden'})


@callback(
    Output('map', 'figure'),
    [Input('crops', 'value')]
)
def update_map(value):
    trace = go.Scattermapbox(
        lat=data['latitude'],
        lon=data['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='red',
        ),
        text=data['market'],
    )
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            center=dict(
                lat=data['latitude'].median(),
                lon=data['longitude'].median()
            ),
            style='open-street-map',
            zoom=4.9,
        ),
        title='Market Locations',
        margin=dict(l=40, r=40, t=40, b=30)
    )
    return {'data': [trace], 'layout': layout}
