import os
from flask import Flask
from flask import redirect, request, url_for
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
from.db.db_queries import get_user_by_id
from .models import User

from dotenv import load_dotenv

load_dotenv()


token= os.environ.get("SECRET_KEY")
csrf = CSRFProtect()
login_manager= LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = token
    login_manager.init_app(app)
    csrf.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)

    @login_manager.user_loader
    def load_user(user_id):
        user_data= get_user_by_id(user_id)
        return User(user_data[0], user_data[1])

    @app.before_request
    def restrict_dash():

        not_without_login= ["/new-athlete", "/results", "/select-athlete"]
        for restricted_route in not_without_login:
            if request.path.startswith(restricted_route) and not current_user.is_authenticated:
                return redirect(url_for("main.login"))
    
    
    return app

