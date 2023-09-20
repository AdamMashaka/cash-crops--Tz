from dash import html, dcc, Output, Input, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sidebar import sidebar
from navbar import navbar


register_page(__name__, path='/visualize/presidency')

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
                        id="presidency-radios",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "2006-2010", "value": "2006-2010"},
                            {"label": "2011-2015", "value": "2011-2015"},
                            {"label": "2016-2020", "value": "2016-2020"},
                            {"label": "2021-2023", "value": "2021-2023"},
                        ],
                        value="2006-2010",
                        style={"float": "right"}
                    ),
                ]),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='presidency-graph',
                                  style={'height': '540px'}),
                    ])
                ],
                style={'boxShadow': '0px 1px 5px #999', 'marginBottom': '25px'})

            ]),
    ])
])


# callback

@callback(
    Output('presidency-graph', 'figure'),
    [Input('presidency-radios', 'value')]
)
def price_trend(value):
    if value == '2006-2010':
        filtered_data = data[(data['year'] >= 2006) & (data['year'] <= 2010)]
        month_commodity_avg = filtered_data.groupby(['month', 'commodity'])['price'].mean().reset_index()
        fig = px.line(
            month_commodity_avg,
            x='month', y='price',
            color='commodity',
            title=f'Average Price of Commodities Over the Months ({value})', labels={'month': 'Month', 'price': 'Average Price'},
            markers='line+markers'
        )
        fig.update_layout(
            xaxis_tickangle=-30,
            margin=dict(l=40, r=40, t=50, b=30),
            title_x=0.5,
            legend_title='Commodity',
        )
        return fig
    
    elif value == '2011-2015':
        filtered_data = data[(data['year'] >= 2011) & (data['year'] <= 2015)]
        month_commodity_avg = filtered_data.groupby(['month', 'commodity'])['price'].mean().reset_index()
        fig = px.line(
            month_commodity_avg,
            x='month', y='price',
            color='commodity',
            title=f'Average Price of Commodities Over the Months ({value})', labels={'month': 'Month', 'price': 'Average Price'},
            markers='line+markers'
        )
        fig.update_layout(
            xaxis_tickangle=-30,
            margin=dict(l=40, r=40, t=50, b=30),
            title_x=0.5,
            legend_title='Commodity',
        )
        return fig
    
    elif value == '2016-2020':
        filtered_data = data[(data['year'] >= 2016) & (data['year'] <= 2020)]
        month_commodity_avg = filtered_data.groupby(['month', 'commodity'])['price'].mean().reset_index()
        fig = px.line(
            month_commodity_avg,
            x='month', y='price',
            color='commodity',
            title=f'Average Price of Commodities Over the Months ({value})', labels={'month': 'Month', 'price': 'Average Price'},
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
    
    if value == '2021-2023':
        filtered_data = data[(data['year'] >= 2021) & (data['year'] <= 2023)]
        month_commodity_avg = filtered_data.groupby(['month', 'commodity'])['price'].mean().reset_index()
        fig = px.line(
            month_commodity_avg,
            x='month', y='price',
            color='commodity',
            title=f'Average Price of Commodities Over the Months ({value})', labels={'month': 'Month', 'price': 'Average Price'},
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
    