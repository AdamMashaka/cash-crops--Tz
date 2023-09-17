import dash_bootstrap_components as dbc
from dash import html,  Output, Input, callback, State, get_asset_url


navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.A(
                        href='/',
                        children=[
                            html.Img(style={'height': '30px', 'borderRadius': '10%', 'overflow': 'hidden'},
                            src=get_asset_url('favicon.ico'))
                        ]
                    ),
                    dbc.NavbarBrand("Crops Price - Tanzania", className='ms-2', href='/')
                ], style={'display': 'flex', 'align-items': 'center'})   
            ],
            align='center')
        ]),

        dbc.Row(dbc.Col(dbc.NavbarToggler(id='nav-toggler', n_clicks=0))),

        dbc.Row([
            dbc.Col([
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Home", href="/", active='exact')),
                            dbc.NavItem(dbc.NavLink("Trend", external_link="/visualize", href='/visualize', active='exact', id='trend-link')),
                            dbc.NavItem(dbc.NavLink("Predict", href="/predict", active='exact')),
                            dbc.NavItem(dbc.DropdownMenu(
                                style={'paddingLeft':'15px'},
                                children=[
                                    dbc.DropdownMenuItem("Map", href='/map'),
                                    dbc.DropdownMenuItem("Github", href='https://github.com/Major2000/FOOD-PRICES-PREDICTION'),
                                    # dbc.DropdownMenuItem("Description", href='/description')
                                ],
                                nav=True,
                                in_navbar=True,
                                label='More'
                            )),
                        ],
                        pills=True,
                        navbar=True,
                    ),
                    id='nav-collapse',
                    navbar=True,
                    is_open=False,)
            ])
        ],
        align='center')
    ]),
    style={'padding': '0px', 'paddingBottom': '5px', 'height':'70px', 'boxShadow': '0px 1px 5px #999'},
    color='rgba(144, 238, 144)',
    fixed='top'
)

@callback(
    Output('nav-collapse', 'is_open'),
    [Input('nav-toggler', 'n_clicks')],
    [State('nav-collapse', 'is_open')]
)

def toggle_bar(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output('trend-link', 'className'),
    [Input('url', 'pathname')]
)
def update_trend_link_classname(pathname):
    if pathname.startswith('/visualize'):
        return 'active'
    return ''