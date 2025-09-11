import pandas as pd
from dash import Input, Output, callback, State, dcc
from dash.exceptions import PreventUpdate
from app.temporal_files_processing import save_uploaded_files
from app.multiprocessing_batch import process_batch


def start_loading_data(app):

    app.layout.children.append(dcc.Location(id="url-after-load", refresh=True))

    @app.callback(
    Output("loading-container", "style"),
    Output("results-store", "data"),
    Output("url-after-load", "href"),

    Input("confirm-load-data-dialog", "submit_n_clicks"),
    Input("athlete-list", "value"),
    State("athlete-raw-data", "data"),
    Input("file-uploader", "contents"),
    Input("file-uploader", "filename")
    )

    def process_and_load_data(submit_n_clicks, selected_athlete, raw_data, contents, filename):

        if not submit_n_clicks:
            raise PreventUpdate

        if submit_n_clicks:
            try:
                filepaths= save_uploaded_files(contents, filename)
                athlete= raw_data[selected_athlete]

                athlete_df= pd.DataFrame([athlete])

                if filepaths:

                    check, success, failures= process_batch(filepaths, athlete_df)

                    if check:

                        results= {"batch_size":len(filepaths), "success": success, "failures":failures}

                        return {"display": "none"}, results, "/dash/results"
                    
                    else: 
                        return {"display": "none"}, {}, "/dash/database-loader/"
                else: 
                    return {"display": "none"}, {}, "/dash/database-loader/"
                    

            except Exception as e:
                print(f"An error occurred during data loading process: {e}")
                return {"display": "none"}, {}, "/dash/database-loader/"

            
