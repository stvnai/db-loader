import pandas as pd
from datetime import date
from dash import dcc, Input, Output, callback
from dash.exceptions import PreventUpdate
from app.db.db_queries import insert_new_athlete



def register_athlete(app):
    app.layout.children.append(dcc.Location(id="url-after-registry", refresh=True))
    @app.callback(
        Output("check-athlete-exist", "displayed"),
        Output("check-athlete-exist", "message"),
        Output("url-after-registry", "href"),
        Input("register-button", "n_clicks"),
        Input("name-input", "value"),
        Input("lastname-input", "value"),
        Input("gender-input", "value"),
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("day-input", "value"),
        
    )

    def check_and_registry_athlete(click_on_register_button, name, last_name, gender, year, month, day):
        if click_on_register_button:
            name= name.lower()
            last_name= last_name.lower()
            gender= gender.lower()

            dob= date(year, month, day)

            athlete_df= pd.DataFrame([
                dict(
                    name=name,
                    last_name=last_name,
                    date_of_birth=dob,
                    gender=gender)
                ]
            )

            confirm_insert= insert_new_athlete(athlete_df)

            if confirm_insert:
                return True, "Athlete registered sucessfully", "/dash/database-loader/"
            
            elif not confirm_insert:
                return True, "Error registering athlete: The athlete already exist", "/dash/register-athlete"
            
            else:
                return True, "An error occurred during registry process. Please try later.", "/dash/register-athlete"

        else:
            raise PreventUpdate    

            

            


