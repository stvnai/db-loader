import os
from pathlib import Path

# Flask
from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

# login management
from .models import User
from .db.db_queries import get_user_by_id

# Dash
from dash import Dash

# layout
from dash_app.select_athlete_layout import db_loader_layout
from dash_app.register_athlete_layout import register_athlete_layout
from dash_app.results_layout import results_layout

# select athlete callbacks
from dash_app.callbacks.athlete_list_callback import load_athletes
from dash_app.callbacks.enable_uploader_callback import enable_uploader
from dash_app.callbacks.confirm_load_data_callback import enable_load_button, confirm_load_data
from dash_app.callbacks.process_and_upload_callback import start_loading_data


# register athlete callbacks
from dash_app.callbacks.day_range_callback import day_range
from dash_app.callbacks.enable_register_button_callback import enable_register_button
from dash_app.callbacks.register_athlete_callback import register_athlete

# result callbacks
from dash_app.callbacks.results_callback import show_results

# log-out callbacks
from dash_app.callbacks.logout_callback import log_out, register_log_out, results_log_out

from dotenv import load_dotenv
load_dotenv()

token= os.environ.get("SECRET_KEY")
csrf = CSRFProtect()
login_manager= LoginManager()


# Flask app

def create_flask_app() -> Flask:

    """
    Description:
    -----
        Creates Flask app with CSRF and Login Mananger

    :return Flask: flask app.

    """

    app = Flask(__name__)
    app.secret_key = token
    login_manager.init_app(app)
    csrf.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)
    csrf._exempt_views.add('dash.dash.dispatch')

    @login_manager.user_loader
    def load_user(user_id):
        user_data= get_user_by_id(user_id)
        return User(user_data[0], user_data[1])

    @app.before_request
    def restrict_dash():

        if request.path.startswith("/dash") and not current_user.is_authenticated:
            return redirect(url_for("main.login"))
    
    
    return app


#Dash App

def create_dash_load_data(flask_app_server: Flask) -> Dash:

    """
    Description
    -----
        Creates dash app into a Flask server to load data to db.

    Args
    -----
    :param (Flask) flask_app_server: Flask server.

    :return Dash: Dash app
    
    """

    assets_path= Path(__file__).parent.parent /"dash_app"/"assets"
    
    dash_app= Dash(
        name="db-loader",
        server= flask_app_server,
        suppress_callback_exceptions= True,
        assets_folder= assets_path,
        url_base_pathname="/dash/database-loader/"
    )

    dash_app.title= "DBLoader Select Athlete"
    dash_app.layout= db_loader_layout

    # Callbacks
    load_athletes(dash_app)
    log_out(dash_app)
    enable_uploader(dash_app)
    enable_load_button(dash_app)
    confirm_load_data(dash_app)
    start_loading_data(dash_app)


    return dash_app


def create_dash_register_athlete(flask_app_server: Flask) -> Dash:

    """
    Description
    -----
        Creates dash app into a Flask server to register athletes in db.

    Args
    -----
    :param (Flask) flask_app_server: Flask server.

    :return Dash: Dash app
    
    """

    assets_path= Path(__file__).parent.parent /"dash_app"/"assets"
    
    dash_app= Dash(
        name="db-loader",
        server= flask_app_server,
        suppress_callback_exceptions= True,
        assets_folder= assets_path,
        url_base_pathname="/dash/register-athlete/"
    )  

    dash_app.title= "DBLoader Register Athlete"
    dash_app.layout= register_athlete_layout

    # Callbacks
    register_log_out(dash_app)
    day_range(dash_app)
    enable_register_button(dash_app)
    register_athlete(dash_app)

    return dash_app

def create_dash_load_results(flask_app_server: Flask) -> Dash:

    """
    Description
    -----
        Creates dash app into a Flask server to display data load results.

    Args
    -----
    :param (Flask) flask_app_server: Flask server.

    :return Dash: Dash app
    
    """

    assets_path= Path(__file__).parent.parent /"dash_app"/"assets"
    
    dash_app= Dash(
        name="db-loader",
        server= flask_app_server,
        suppress_callback_exceptions= True,
        assets_folder= assets_path,
        url_base_pathname="/dash/results/"
    )  

    dash_app.title= "DBLoader Results"
    dash_app.layout= results_layout

    # Callbacks
    results_log_out(dash_app)
    show_results(dash_app)


    return dash_app
