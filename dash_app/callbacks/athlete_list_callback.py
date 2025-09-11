from dash import Input, Output, State, callback
from app.db.db_queries import athlete_list


def load_athletes(app):
    @app.callback(
        Output("athlete-list", "options"),
        Output("athlete-raw-data", "data"),
        Input("athlete-list", "id")
    )
    def query_athletes(_):

        try:
            visible_labels, raw_data= athlete_list()

            options= [{"label": label, "value": i} for i, label in enumerate(visible_labels)]

            return options, raw_data
        
        except Exception as e:
            error_option= [{"label":"Error loading athletes", "value": None}]
            return error_option
