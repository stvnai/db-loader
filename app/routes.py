
# forms
from app.forms import LoginForm

#db queries
from app.db.db_queries import auth_user

#logggin
from app.set_logging import set_module_logger

# Flask
from flask import Blueprint, render_template, redirect, url_for, flash

# users management
from .models import User
from flask_login import login_user, logout_user, login_required


logger=set_module_logger(__name__)
main= Blueprint("main", __name__)


@main.route('/')
def index():
    return redirect(url_for('main.login'))

### LOGIN ROUTE ###

@main.route("/login", methods=["GET", "POST"])
def login():

    login_form= LoginForm()

    if login_form.validate_on_submit():

        username= login_form.username.data
        password= login_form.password.data

        user_id= auth_user(username, password)

        if user_id is not None:
            user= User(user_id, username)
            login_user(user)
            return redirect("/dash/database-loader/")
        
        
        else:
            flash("Wrong username or password.", "danger")
            return redirect(url_for("main.login"))

    return render_template("login.html", login_form=LoginForm())



### LOGOUT ###

@main.route("/logout")
@login_required


def logout():
    
    """Close session and redirect to /login"""

    logout_user()
    return redirect(url_for("main.login"))








