from dash import html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "bottom": "0",
    "width": "12rem",
    "padding": "2rem 0.5rem",
    "background-color": "#f8f9fa",
    'boxShadow': '0px 1px 5px #999',
    'fontFamily': 'sans-serif',
    'display': 'flex',
    'flexDirection': 'column',
}

sidebar = html.Div(
    [
        html.H2("Visualize", className="display-7",
                style={'paddingTop': '70px', 'textAlign': 'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Data Repository", href="/visualize/data", active="exact"),
                dbc.NavLink("Market Volume",
                            href="/visualize/market-volume", active="exact"),
                dbc.NavLink("Crops Price Trend", href="/visualize/price-trend",
                            active="exact"),
                dbc.NavLink("Market Price Trend",
                            href="/visualize/market-price", active="exact"),
                dbc.NavLink("High and Low Price",
                            href="/visualize/high-low-prices", active="exact"),
                dbc.NavLink("Presidency Trend",
                            href="/visualize/presidency", active="exact"),
                dbc.NavLink("Crop Price Dist..",
                            href="/visualize/crop-distribution", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)