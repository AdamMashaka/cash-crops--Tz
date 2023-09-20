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
    filtered_data = data[data['commodity'].isin(['Maize', 'Beans', 'Rice'])]
    trace = go.Scattermapbox(
        lat=filtered_data['latitude'],
        lon=filtered_data['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='red',
        ),
        text=filtered_data.apply(lambda row: f"{row['market']}<br>Average Maize Price: {filtered_data[(filtered_data['commodity'] == 'Maize') & (filtered_data['market'] == row['market'])]['price'].mean():,.2f}<br>Average Beans Price: {filtered_data[(filtered_data['commodity'] == 'Beans') & (filtered_data['market'] == row['market'])]['price'].mean():,.2f}<br>Average Rice Price: {filtered_data[(filtered_data['commodity'] == 'Rice') & (filtered_data['market'] == row['market'])]['price'].mean():,.2f}", axis=1),
    )
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            center=dict(
                lat=filtered_data['latitude'].median(),
                lon=filtered_data['longitude'].median()
            ),
            style='open-street-map',
            zoom=4.9,
        ),
        title='Market Locations',
        margin=dict(l=40, r=40, t=40, b=30)
    )
    return {'data': [trace], 'layout': layout}
