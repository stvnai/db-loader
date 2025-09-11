from dash import Input, Output, State, callback


def enable_uploader(app):
    @app.callback(
            Output("file-uploader", "disabled"),
            Input("athlete-list", "value"),
            Input("athlete-raw-data", "data"),

    )

    def uploader_enabled(selected_index, raw_data):
        if selected_index is None or not raw_data:
            return True
        else:
            return False