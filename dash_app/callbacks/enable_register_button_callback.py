from dash import Input, Output, callback, dcc

def enable_register_button(app):
    @app.callback(
        Output("register-button", "disabled"),
        Input("name-input", "value"),
        Input("lastname-input", "value"),
        Input("gender-input", "value"),
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("day-input", "value"),
    )

    def activate_button(name, lastname, gender, year, month, day):
        if all([name, lastname, gender, year, month, day]):
            return False
        else:
            return True