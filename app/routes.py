import os
import tempfile
import pandas as pd
from app.db.db_queries import auth_user, athlete_list, insert_new_athlete
from app.forms import InputForm, LoginForm, UploadFiles
from werkzeug.utils import secure_filename
from app.set_logging import set_module_logger
from app.multiprocessing_batch import process_batch
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, get_flashed_messages
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
            return redirect(url_for("main.select_athlete"))
        
        
        else:
            flash("Wrong username or password.", "danger")
            return redirect(url_for("main.login"))

    return render_template("login.html", login_form=LoginForm())


### SELECT AND UPLOAD ATHLETE

@main.route("/select-athlete", methods=["GET","POST"])
@login_required
def select_athlete():


    visible_labels, raw_data= athlete_list()
    session["athlete_data"]= raw_data

    form= UploadFiles()

    if form.validate_on_submit():
        
        files= form.file_upload.data
        index= int(request.form["athlete_index"])
        selected_athlete= session["athlete_data"][index]

        athlete_df= pd.DataFrame([selected_athlete]) 
        logger.info(f"Batch size: {len(files)}")

        filepaths= []
        for file in files:
            filename= secure_filename(file.filename)

            with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
                file.save(tmp)
                filepath= tmp.name

                filepaths.append(filepath)

        session["batch_size"]= len(filepaths)

        if filepaths:
            check, successes, failures= process_batch(filepaths, athlete_df)
            session["successes"]= successes
            session["failures"]= failures
            session["check"]= check
        
        if check and failures == 0:
            flash("Batch processed. All files loaded sucessfully.", "success")
            return redirect(url_for("main.results"))
        
        elif check and failures > 0:
            flash("Batch processed. Some files were not uploaded.", "warning")
            return redirect(url_for("main.results"))
        
        
        elif not check:
            logger.error("Error proccesing batch.")
            flash("Files not uploaded.", "danger")
            return redirect(url_for("main.results"))


    return render_template("select-athlete.html", visible_labels = visible_labels, form= form)



### REGISTER ATHLETE ###

@main.route("/new-athlete", methods=["GET","POST"])
@login_required
def new_athlete():

    form= InputForm()

    if form.validate_on_submit():
        logger.info("Data from register athlete form retrieved successfully")

        name= form.name.data.lower()
        last_name= form.last_name.data.lower()
        dob= form.date_of_birth.data
        gender= form.gender.data.lower()
    

        athlete_df= pd.DataFrame([
            dict(
                name=name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender)]
        ) 

        check_insert= insert_new_athlete(athlete_df)

        if check_insert:
            flash("Athlete registered successfully.", "success")
            return redirect(url_for("main.select_athlete"))
        
        elif not check_insert:
            flash("Trying to register an already existing athlete.", "danger")
            return redirect(url_for("register_athlete.index"))
        
        else:
            flash("Error trying to register athlete.", "danger")
            return redirect(url_for("register_athlete.index"))

    else:
        logger.warning("Form did not validate.")
        logger.debug(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                logger.error(f"Validation error in '{field}': {error}")
        
    return render_template("register-athlete.html", form= form)


### RESULTS ###

@main.route("/results", methods=["GET"])
@login_required
def results():

    success= session.pop("successes", None)
    fails= session.pop("failures", None)
    check= session.pop("check", None)
    batch_size= session.pop("batch_size", None)
    if not check:
        return redirect(url_for("main.select_athlete"))
      
    return render_template("results.html",  success= success, fails= fails, batch_size=batch_size) 

### LOGOUT ###

@main.route("/logout")
@login_required


def logout():
    
    """Close session and redirect to /login"""

    logout_user()
    return redirect(url_for("main.login"))








