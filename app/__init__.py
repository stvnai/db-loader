import os
from flask import Flask



def create_app():
    app = Flask(__name__)
    from .routes import main
    app.register_blueprint(main)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    
    return app

