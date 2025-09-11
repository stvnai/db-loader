from dash import Input, Output, dcc
from flask import url_for


def log_out(app):
    app.layout.children.append(dcc.Location(id="url-logout", refresh=True))

    @app.callback(
        Output("url-logout", "href"),
        Input("logout-button", "n_clicks"),
        prevent_initial_call=True
    )

    def handle_logout(n_clicks):
        if n_clicks:

            return url_for("main.logout")

def register_log_out(app):
    app.layout.children.append(dcc.Location(id="register-url-logout", refresh=True))

    @app.callback(
        Output("register-url-logout", "href"),
        Input("register-logout-button", "n_clicks"),
        prevent_initial_call=True
    )

    def handle_logout(n_clicks):
        if n_clicks:

            return url_for("main.logout")
        
def results_log_out(app):
    app.layout.children.append(dcc.Location(id="results-url-logout", refresh=True))

    @app.callback(
        Output("results-url-logout", "href"),
        Input("results-logout-button", "n_clicks"),
        prevent_initial_call=True
    )

    def handle_logout(n_clicks):
        if n_clicks:

            return url_for("main.logout")


