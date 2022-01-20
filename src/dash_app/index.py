import os
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash_app.app import app

from dash_app.network_simulation import layout as network_simulation_page

navbar = dbc.NavbarSimple(
    children=[dbc.NavItem(dbc.NavLink("About Us", href="#"))],
    brand="Metapopulation Network Models for COVID-19",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    return network_simulation_page


if __name__ == "__main__":
    app.run_server(debug=True, port=os.getenv("PORT", "8051"))
