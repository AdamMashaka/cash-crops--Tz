from dash import Dash, html, dcc, Output, Input, page_container
import dash_bootstrap_components as dbc


app = Dash(
    __name__,
    update_title="Loading...",
    title='Crops Price - Tanzania',
    external_stylesheets=[dbc.themes.LITERA, './assets/styles.css'],
    use_pages=True,
)

server = app.server

app.layout = html.Div(
    [
        dcc.Loading(
            id="loading-spinner",
            type="default",
            fullscreen=True,
            children=[
                page_container,
            ],
        ),
    ],
)

if __name__ == '__main__':
    app.run(debug=True)