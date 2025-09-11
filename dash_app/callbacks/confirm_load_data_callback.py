from dash import Input, Output, State, dcc, callback

from dash.exceptions import PreventUpdate

def enable_load_button(app):
    @app.callback(
    Output("load-button", "disabled"),
    Input("file-uploader", "contents"),
    Input("athlete-list", "value")
    )

    def button_enabled(files, selected_option):
        if selected_option is None or not files:
            
            return True
        
        else:
            return False


def confirm_load_data(app):
    @app.callback(
#         
        Output("confirm-load-data-dialog", "message"),
        Input("file-uploader", "contents"),
        Input("athlete-list", "value"),
        State("athlete-list", "options")
    )

    def confirm_load(files, athlete_selected, options):

        if not files or athlete_selected is None:
            raise PreventUpdate
        
        else:
            try:
                selected_option=options[athlete_selected]
                return f"Load data to {selected_option.get("label", "No data")}?"
            except Exception:
                raise PreventUpdate
   
        
