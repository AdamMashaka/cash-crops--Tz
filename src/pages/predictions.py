from dash import html, dcc, Output, Input, register_page, callback, dash_table, State
import dash_bootstrap_components as dbc
import pandas as pd
import pickle as pk
import plotly.express as px
import numpy as np
from navbar import navbar
import warnings
import requests
warnings.filterwarnings('ignore')

register_page(__name__, path='/predict')

data = pd.read_csv('../Data/needed_food_data.csv')
Maize_data = pd.read_csv('../Data/maize.csv')
Beans_data = pd.read_csv('../Data/beans.csv')
Rice_data = pd.read_csv('../Data/rice.csv')

maize_model = pk.load(open('../Models/Maize/Maize_model_XGBoost Regressor.pkl', 'rb'))
beans_model = pk.load(open('../Models/Beans/Beans_model_XGBoost Regressor.pkl', 'rb'))
rice_model = pk.load(open('../Models/Rice/Rice_model_XGBoost Regressor.pkl', 'rb'))

columns = [col for col in data.columns if col not in [
    'latitude', 'longitude', 'price', 'unit']]


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
                        pd.Timestamp.now().year, pd.Timestamp.now().year + 2)],
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
    
    inputs = {}

    column_order = [
        'market',
        'year',
        'month',
        'years_since_start',
        'past_1_months_mean_price',
        'past_2_months_mean_price',
        'past_3_months_mean_price',
        'past_4_months_mean_price',
        'past_5_months_mean_price',
        'past_6_months_mean_price',
        'past_7_months_mean_price',
        'past_8_months_mean_price',
        'past_9_months_mean_price',
        'past_10_months_mean_price',
        'past_11_months_mean_price',
        'past_1_years_mean_price',
        'past_2_years_mean_price',
        'past_3_years_mean_price',
        'past_4_years_mean_price',
        'past_5_years_mean_price',
        'past_6_years_mean_price',
        'past_7_years_mean_price',
        'past_8_years_mean_price',
        'past_9_years_mean_price',
        'past_10_years_mean_price',
        'past_11_years_mean_price',
        'past_12_years_mean_price',
        'past_13_years_mean_price',
        'past_14_years_mean_price',
        'past_15_years_mean_price',
        'past_16_years_mean_price',
        'past_17_years_mean_price',
        'yearly_average_price',
        'monthly_average_price',
        'market_average_price',
        'commodity_yearly_average_price',
        'commodity_monthly_average_price'
    ]

    market_mapping = {
        'Arusha (urban)': 0,
        'Babati': 1,
        'Bukoba': 2,
        'Dar es Salaam - Ilala': 3,
        'Dar es Salaam - Kinondoni': 4,
        'Dodoma (Kibaigwa)': 5,
        'Dodoma (Majengo)': 6,
        'Morogoro': 7,
        'Mpanda': 8,
        'Mtwara DC': 9,
        'Musoma': 10,
        'Tabora': 11,
        'Tanga / Mgandini': 12
    }

    def pipelineInput(inputDict):

        inputDict['market'] =market_mapping.get(str(selected_market))

        inputDict['year'] = [int(selected_year)]

        inputDict['month'] = [int(selected_month)]

        inputDict['years_since_start'] = int(selected_year) - 2006

        if selected_crop == 'Maize':
            if str(selected_market) not in Maize_data['market']:
                most_recent_year = int(selected_year) - 3
            else:
                 most_recent_year = int(selected_year) - 1
            filtered_data = Maize_data[(Maize_data['market'] == market_mapping.get(str(selected_market))) &
                                        (Maize_data['year'] == most_recent_year)]
            
            inputDict['yearly_average_price'] = filtered_data['yearly_average_price'].mode()

            if int(selected_month) in filtered_data['month'].unique():
                inputDict['monthly_average_price'] = filtered_data.loc[filtered_data['month'] == int(selected_month)]['market_average_price'].reset_index(drop=True)
            else:
                inputDict['monthly_average_price'] = filtered_data['monthly_average_price'].mean()
            
            inputDict['market_average_price'] = filtered_data['market_average_price'].mode()

            inputDict['commodity_yearly_average_price'] = filtered_data['commodity_yearly_average_price'].mode()

            if int(selected_month) in filtered_data['month'].unique():
                inputDict['commodity_monthly_average_price'] = filtered_data.loc[filtered_data['month'] == int(selected_month)]['commodity_monthly_average_price'].reset_index(drop=True)
            else:
                inputDict['commodity_monthly_average_price'] = filtered_data['commodity_monthly_average_price'].mean()
            
            filtered_data = filtered_data.drop(['market', 'year', 'month', 'years_since_start', 'yearly_average_price', 'monthly_average_price', 'market_average_price', 'commodity_yearly_average_price', 'commodity_monthly_average_price'], axis=1)
            
            for col in filtered_data.columns:
                inputDict[col] = filtered_data[col].mean()

        elif selected_crop == 'Beans':
            if str(selected_market) not in Beans_data['market']:
                most_recent_year = int(selected_year) - 3
            else:
                 most_recent_year = int(selected_year) - 1
            filtered_data = Beans_data[(Beans_data['market'] == market_mapping.get(str(selected_market))) &
                                        (Beans_data['year'] == most_recent_year)]
            
            inputDict['yearly_average_price'] = filtered_data['yearly_average_price'].mode()

            if int(selected_month) in filtered_data['month'].unique():
                inputDict['monthly_average_price'] = filtered_data.loc[filtered_data['month'] == int(selected_month)]['market_average_price'].reset_index(drop=True)
            else:
                inputDict['monthly_average_price'] = filtered_data['monthly_average_price'].mean()
            
            inputDict['market_average_price'] = filtered_data['market_average_price'].mode()

            inputDict['commodity_yearly_average_price'] = filtered_data['commodity_yearly_average_price'].mode()

            if int(selected_month) in filtered_data['month'].unique():
                inputDict['commodity_monthly_average_price'] = filtered_data.loc[filtered_data['month'] == int(selected_month)]['commodity_monthly_average_price'].reset_index(drop=True)
            else:
                inputDict['commodity_monthly_average_price'] = filtered_data['commodity_monthly_average_price'].mean()
            
            filtered_data = filtered_data.drop(['market', 'year', 'month', 'years_since_start', 'yearly_average_price', 'monthly_average_price', 'market_average_price', 'commodity_yearly_average_price', 'commodity_monthly_average_price'], axis=1)
            
            for col in filtered_data.columns:
                inputDict[col] = filtered_data[col].mean()

        elif selected_crop == 'Rice':
            if str(selected_market) not in Rice_data['market']:
                most_recent_year = int(selected_year) - 3
            else:
                 most_recent_year = int(selected_year) - 1
            filtered_data = Rice_data[(Rice_data['market'] == market_mapping.get(str(selected_market))) &
                                        (Rice_data['year'] == most_recent_year)]
            
            inputDict['yearly_average_price'] = filtered_data['yearly_average_price'].mode()

            if int(selected_month) in filtered_data['month'].unique():
                inputDict['monthly_average_price'] = filtered_data.loc[filtered_data['month'] == int(selected_month)]['market_average_price'].reset_index(drop=True)
            else:
                inputDict['monthly_average_price'] = filtered_data['monthly_average_price'].mean()
            
            inputDict['market_average_price'] = filtered_data['market_average_price'].mode()

            inputDict['commodity_yearly_average_price'] = filtered_data['commodity_yearly_average_price'].mode()

            if int(selected_month) in filtered_data['month'].unique():
                inputDict['commodity_monthly_average_price'] = filtered_data.loc[filtered_data['month'] == int(selected_month)]['commodity_monthly_average_price'].reset_index(drop=True)
            else:
                inputDict['commodity_monthly_average_price'] = filtered_data['commodity_monthly_average_price'].mean()
            
            filtered_data = filtered_data.drop(['market', 'year', 'month', 'years_since_start', 'yearly_average_price', 'monthly_average_price', 'market_average_price', 'commodity_yearly_average_price', 'commodity_monthly_average_price'], axis=1)
            
            for col in filtered_data.columns:
                inputDict[col] = filtered_data[col].mean()

        return pd.DataFrame(inputDict, columns=column_order)


    predicted_price = None

    inputs = {}

    if selected_crop == 'Maize':
        predicted_price = maize_model.predict(pipelineInput(inputDict= inputs))[0]
    elif selected_crop == 'Beans':
        predicted_price = beans_model.predict(pipelineInput(inputDict= inputs))[0]
    elif selected_crop == 'Rice':
        predicted_price = rice_model.predict(pipelineInput(inputDict= inputs))[0]
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