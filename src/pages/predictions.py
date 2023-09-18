from dash import html, dcc, Output, Input, register_page, callback, dash_table, State
import dash_bootstrap_components as dbc
import pandas as pd
import pickle as pkl
import plotly.express as px
import numpy as np
from navbar import navbar
import warnings
import requests
warnings.filterwarnings('ignore')

register_page(__name__, path='/predict')

data = pd.read_csv('../Data/needed_food_data.csv')


columns = [col for col in data.columns if col not in [
    'latitude', 'longitude', 'price', 'unit']]



# maize_url = 'https://drive.google.com/uc?export=download&id=1C23g0GnUcVilDHJetYFyZdpUOugU2JQW'
# beans_url = 'https://drive.google.com/uc?export=download&id=1Qvn3zD0OR-5cyB1UioHDDFFG26nELmJg'
# rice_url = 'https://drive.google.com/uc?export=download&id=1bmVKarTIY-M4M1FU-ZzqJ5s1ppAuO5pL'

# def download_model(url, filename):
#     response = requests.get(url)
#     with open(filename, 'wb') as f:
#         f.write(response.content)

# download_model(maize_url, 'maize_model.pkl')
# download_model(beans_url, 'beans_model.pkl')
# download_model(rice_url, 'rice_model.pkl')



maize_model = pkl.load(open('../Models/Maize/Maize_model_CatBoost Regressor.pkl', 'rb'))
# beans_model = pkl.load(open('beans_model.pkl', 'rb'))
# rice_model = pkl.load(open('rice_model.pkl', 'rb'))


def generate_input_data(selected_market, selected_crop, selected_month, selected_year):
    data = {
        'market': [selected_market],
        'commodity': [selected_crop],
        'month': [selected_month],
        'year': [selected_year],
    }

    return pd.DataFrame(data)


# sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "bottom": "0",
    "width": "17rem",
    "padding": "2rem 0.5rem",
    "background-color": "#f8f9fa",
    'boxShadow': '0px 1px 5px #999',
    'fontFamily': 'sans-serif',
    'display': 'flex',
    'flexDirection': 'column',
}

sidebar = html.Div(
    [
        html.H2("Parameters", className="display-7",
                style={'paddingTop': '60px', 'textAlign': 'center'}),
        html.Hr(),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'column', 'gap': '50px'},
            children=[
                dcc.Dropdown(
                    id='market-dropdown',
                    options=[{'label': market, 'value': market}
                             for market in data['market'].unique()],
                    placeholder="Select Market",
                ),

                dcc.Dropdown(
                    id='crop-dropdown',
                    options=[{'label': crop, 'value': crop}
                             for crop in data['commodity'].unique()],
                    placeholder="Select Crop"
                ),
                
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': year, 'value': year} for year in range(
                        pd.Timestamp.now().year, pd.Timestamp.now().year + 3)],
                    placeholder="Select Year"
                ),

                dcc.Dropdown(
                    id='month-dropdown',
                    placeholder="Select Month"
                ),

                dbc.Button("Forecast Price", color="primary",
                           id='predict-button', n_clicks=0, disabled=True),
            ]
        ),
    ],
    style=SIDEBAR_STYLE,
)


# Layout
layout = dbc.Container([
    navbar,
    dbc.Row([
        sidebar,

        html.Div(
            style={'paddingTop': '100px', 'paddingLeft': '280px',
                   'paddingRight': '30px', 'display': 'grid', 'gap': '25px', },

            children=[
                dbc.Card([
                    dbc.CardHeader(
                        "Input Parameters",
                        style={
                            'textShadow': '2px 2px 4px rgba(0,0,0,0.4)',
                            "fontFamily": "sans-serif",
                            "textAlign": "center",
                        },
                    ),
                    dbc.CardBody([
                        dash_table.DataTable(
                            id='input-table',
                            columns=[
                                {'name': column, 'id': column} for column in columns
                            ],
                            style_header={
                                'fontWeight': 'bold',
                                'textAlign': 'center',
                                'textTransform': 'capitalize',
                                'backgroundColor': 'rgba(211, 211, 211, 0.7)',
                                'textShadow': '2px 2px 4px rgba(0,0,0,0.4)',
                                'fontSize': '14px'
                            },
                            style_data={
                                'textAlign': 'center',
                                'fontWeight': '200',
                                'fontSize': '12px',
                                'fontFamily': "Lucida Sans Typewriter",
                            },
                        ),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999'}),


                dbc.Card([
                    dbc.CardHeader(
                        "Predicted Price (100KG)",
                        style={
                            'backgroundColor': 'rgba(211, 211, 211, 0.4)',
                            'textShadow': '2px 2px 4px rgba(0,0,0,0.4)',
                            "fontFamily": "sans-serif",
                            "textAlign": "center",
                        },
                    ),
                    dbc.CardBody(
                        [
                            html.Div(
                                id='predicted-price',
                                style={
                                    "fontSize": "36px",
                                    'textShadow': '2px 2px 4px rgba(0,0,0,0.4)',
                                    "fontFamily": "Abril Fatface",
                                    "textAlign": "center",
                                },
                            )
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "height": "100%",
                        },
                    )
                ], style={
                    'boxShadow': '0px 1px 5px #999', 
                    "width": "30rem",
                    "height": "15rem",
                    "margin": "auto",
                }),

                html.Div(
                    [
                        dbc.RadioItems(
                            id="radios",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "Market", "value": "Market"},
                                {"label": "Monthly", "value": "Monthly"},
                                {"label": "Yearly", "value": "Yearly"},
                            ],
                            value="Market",
                            style={"float": "right"}
                        ),
                    ],
                ),

                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='price-trend-graph',
                                  style={'height': '540px'}),
                    ])
                ], style={'boxShadow': '0px 1px 5px #999', 'marginBottom': '25px'})
            ])
    ])
])


# Callbacks


@callback(
    [
        Output('predict-button', 'disabled'),
        Output('predict-button', 'style')
    ],

    [
        Input('market-dropdown', 'value'),
        Input('crop-dropdown', 'value'),
        Input('month-dropdown', 'value'),
        Input('year-dropdown', 'value')
    ]
)
def enable_disable_button(selected_market, selected_crop, selected_month, selected_year):
    all_dropdowns_filled = all(
        [selected_market, selected_crop, selected_month, selected_year])

    button_style = {
        'backgroundColor': 'rgba(144, 238, 144)',
        'boxShadow': '0px 1px 5px #999',
        'color': 'black',
        'display': 'block',
        'margin': 'auto',
        'marginTop': '50%',
        'borderColor': 'green' if all_dropdowns_filled else 'red'
    }

    return not all_dropdowns_filled, button_style


@callback(
    Output('input-table', 'data'),
    Input('market-dropdown', 'value'),
    Input('crop-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    Input('year-dropdown', 'value'),
)
def update_input_table(selected_market, selected_crop, selected_month, selected_year):
    data = generate_input_data(
        selected_market, selected_crop, selected_month, selected_year)
    table_data = data.to_dict('records')

    return table_data


@callback(
    Output('predicted-price', 'children'),

    Input('predict-button', 'n_clicks'),
    State('crop-dropdown', 'value'),
    State('market-dropdown', 'value'),
    State('month-dropdown', 'value'),
    State('year-dropdown', 'value')
)
def predict_price(n_clicks, selected_crop, selected_market, selected_month, selected_year):
    if n_clicks is None:
        return None

    column_order = [
        'year', 'month', 'market_Arusha (urban)', 'market_Babati',
        'market_Bukoba', 'market_Dar es Salaam - Ilala', 'market_Dar es Salaam - Kinondoni',
        'market_Dodoma (Kibaigwa)', 'market_Dodoma (Majengo)', 'market_Morogoro',
        'market_Mpanda', 'market_Mtwara DC', 'market_Musoma', 'market_Tabora', 'market_Tanga / Mgandini'
    ]

    inputs = pd.DataFrame(columns=column_order)

    inputs['year'] = [selected_year]
    inputs['year'] = np.log10(inputs['year'])

    inputs['month'] = [selected_month]

    for market_col in column_order[2:]:
        inputs[market_col] = 0

    if selected_market:
        inputs[f'market_{selected_market}'] = 1

    predicted_price = None

    if selected_crop == 'Maize':
        predicted_price = maize_model.predict(inputs)
    elif selected_crop == 'Beans':
        predicted_price = beans_model.predict(inputs)
    elif selected_crop == 'Rice':
        predicted_price = rice_model.predict(inputs)

    if predicted_price is not None:
        return f'TZS {float(predicted_price):,.2f}'

    return ''


@callback(
    Output('price-trend-graph', 'figure'),
    [Input('crop-dropdown', 'value'), Input('radios', 'value')]
)
def update_graph(crop, radio):
    if radio == 'Monthly':
        average_prices = data.groupby(['month', 'commodity'])[
            'price'].mean().reset_index()
        df = average_prices[average_prices['commodity'] == crop]
        fig = px.line(df, x='month', y='price', markers='line+markers', color_discrete_sequence=['orangered'])
        fig.update_layout(
            xaxis=dict(title='Month'),
            yaxis=dict(title='Average Price'),
            xaxis_tickangle=-45,
            margin=dict(l=40, r=40, t=50, b=50),
            title=f'Average Price Trends for {crop}',
            title_x=0.5,
            title_y=0.96,
        )
        return fig
    elif radio == "Yearly":
        average_prices = data.groupby(['year', 'commodity'])[
            'price'].mean().reset_index()
        df = average_prices[average_prices['commodity'] == crop]
        fig = px.line(df, x='year', y='price', markers='line+markers', color_discrete_sequence=['blue'])
        fig.update_layout(
            xaxis=dict(title='Year'),
            yaxis=dict(title='Average Price'),
            xaxis_tickangle=-45,
            margin=dict(l=40, r=40, t=50, b=50),
            title=f'Average Price Trends for {crop}',
            title_x=0.5,
            title_y=0.96,
        )
        return fig
    else:
        average_prices = data.groupby(['market', 'commodity'])[
            'price'].mean().reset_index()
        df = average_prices[average_prices['commodity'] == crop]
        fig = px.line(df, x='market', y='price', markers='line+markers', color_discrete_sequence=['seagreen'])
        fig.update_layout(
            xaxis=dict(title='Year'),
            yaxis=dict(title='Average Price'),
            xaxis_tickangle=-45,
            margin=dict(l=40, r=40, t=50, b=50),
            title=f'Average Price Trends for {crop}',
            title_x=0.5,
            title_y=0.96,
        )
        return fig


@callback(
    Output('month-dropdown', 'options'),
    Input('year-dropdown', 'value')
)
def month_values(value):
    if str(pd.Timestamp.now().year) == str(value):
        return [{'label': month, 'value': month} for month in range(pd.Timestamp.now().month + 1, 13)]
    else:
        return [{'label': month, 'value': month} for month in range(1, 13)]