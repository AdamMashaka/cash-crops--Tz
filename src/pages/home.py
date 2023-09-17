from dash import Dash, html, register_page, get_asset_url
import dash_bootstrap_components as dbc
from navbar import navbar

register_page(__name__, path='/', title='Crops Price - Tanzania',)

layout = html.Div(
    [
        navbar,
        html.Div(
            style={'padding': '70px', 'paddingTop': '100px', 'height': 'calc(100vh - 30px)', 'flexDirection': 'column',
                   'display': 'flex', 'gap': '50px', 'justifyContent': 'center', 'alignItems': 'center'},
            children=[
                html.H2(children='Welcome to Tanzania Crops Price Dashboard', style={
                        'textAlign': 'center', 'margin': '30px', 'paddingTop': '20px'}),

                html.Div(style={'display': 'flex', 'gap': '50px'}, children=[
                    html.A(href='/visualize', style={'textDecoration': 'none'}, children=[
                        dbc.Card(
                                [
                                    dbc.CardImg(
                                        src=get_asset_url('trend.jpg'), top=True),
                                    dbc.CardBody(
                                        [
                                            html.H4("View Trend",
                                                    className="card-title"),
                                            html.P(
                                                "Take a deep dive into the historical price trends of various crops in Tanzania, spanning from the past to the present day.",
                                                className="card-text",
                                            ),
                                            dbc.Button(
                                                "Visualize", color="primary", external_link='/visualize', style={'marginBottom': '5%', 'marginLeft': 'auto', 'backgroundColor': 'rgba(144, 238, 144)', 'boxShadow': '0px 1px 5px #999', 'color':'black', 'borderColor':'green'}),
                                        ],
                                        style={'backgroundColor': 'rgba(144, 238, 144, 0.3)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between', 'height': '100%'}
                                    ),
                                ],
                            style={"width": "23rem", 'height': '30rem',
                                   'boxShadow': '0px 1px 5px #999'},
                        )
                    ]),
                    html.A(href='/predict', style={'textDecoration': 'none'}, children=[
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    src=get_asset_url('predict.jpg'), top=True, style={'height':'210px'}),
                                dbc.CardBody(
                                    [
                                        html.H4("Forecast Price",
                                                className="card-title"),
                                        html.P(
                                            "Unlock the power of predictive analytics and forecast crop prices for upcoming seasons, months, and even years with our advanced prediction tool.",
                                            className="card-text",
                                            style={'paddingBottom': '0px'}
                                        ),
                                        dbc.Button(
                                            "Forecast", color="primary", href='/predict', style={'marginBottom': '5%', 'marginLeft': 'auto', 'backgroundColor': 'rgba(144, 238, 144)', 'boxShadow': '0px 1px 5px #999', 'color':'black', 'borderColor':'green'}),
                                    ], 
                                    style={'backgroundColor': 'rgba(144, 238, 144, 0.3)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between', 'height': '100%'}
                                ),
                            ],
                            style={"width": "23rem", 'height': '30rem',
                                   'boxShadow': '0px 1px 5px #999'},
                        )
                    ]),

                    html.A(href='/map', style={'textDecoration': 'none'}, children=[
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    src=get_asset_url('Tanzania.jpg'), style={ 'height': '20rem'}),
                                dbc.CardImgOverlay(
                                    [
                                        html.H4("View Map",
                                                className="card-title", style={'marginTop':'80%'}),
                                        html.P(
                                            "Explore the geographical distribution of various markets across Tanzania with our interactive map.",
                                            className="card-text",
                                        ),
                                        dbc.Button(
                                            "Go to map", color="primary", href='/map', style={'marginBottom': '5%', 'marginLeft': 'auto', 'backgroundColor': 'rgba(144, 238, 144)', 'boxShadow': '0px 1px 5px #999', 'color':'black', 'borderColor':'green'}),
                                    ],
                                    style={'backgroundColor': 'rgba(144, 238, 144, 0.3)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between', 'height': '100%'}
                                ),
                            ],
                            style={"width": "23rem", 'height': '30rem',
                                   'boxShadow': '0px 1px 5px #999'},
                        )
                    ]),
                ]),
            ]
        ),
    ]
)
