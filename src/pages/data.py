from dash import html, dcc, Output, Input, register_page, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from sidebar import sidebar
from navbar import navbar


register_page(__name__, path='/visualize/data', redirect_from=['/visualize'])

data = pd.read_csv('../Data/needed_food_data.csv')


layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    html.Div(children=[
        sidebar,

        html.Div(
            style={'paddingTop': '95px', 'paddingLeft': '230px',
                   'paddingRight': '30px', 'display': 'grid', 'gap': '25px', 'height':'calc(100vh - 130px)'},

            children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H3(children='Data Table', style={
                            'textAlign': 'center', 'fontFamily': 'sans-serif'}),
                        dcc.Dropdown(
                            id='column',
                            options=[{'label': column, 'value': column}
                                     for column in data.columns],
                            value=data.columns,
                            multi=True,
                        ),
                        dcc.Markdown('##'),
                        dash_table.DataTable(
                            id='data-table',
                            columns=[
                                {'name': column, 'id': column} for column in data.columns
                            ],
                            data=data.to_dict('records'),
                            page_size=15,
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
                ], style={'boxShadow': '0px 1px 5px #999', 'marginBottom': '5px'}),
            ]
        )
    ]
    )
]
)

# callback
@callback(
    [Output('data-table', 'data'),
     Output('data-table', 'columns')],
    [Input('column', 'value')]
)
def update_table(selected_columns):
    filtered_data = data[selected_columns]
    columns = [{'name': column, 'id': column} for column in selected_columns]
    return filtered_data.to_dict('records'), columns

