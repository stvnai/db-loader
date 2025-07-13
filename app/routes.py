import os
import tempfile
import pandas as pd
from app.forms import InputForm, LoginForm
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators.auth_decorators import login_required
from app.db.user_queries import auth_user
from werkzeug.utils import secure_filename
from app.multiprocessing_batch import process_batch

main= Blueprint("main", __name__)

### LOGIN ROUTE ###

@main.route("/login", methods=["GET", "POST"])
def login():
    login_form= LoginForm()

    if login_form.validate_on_submit():

        username= login_form.username.data
        password= login_form.password.data

        user_id= auth_user(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect(url_for("main.index"))
        
        
        else:
            flash("Wrong username or password.", "danger")
            return redirect(url_for("main.login"))

    return render_template("login.html", login_form=LoginForm())



### MAIN FORM ###

@main.route("/", methods=["GET", "POST"])
@login_required
def index():

    form= InputForm()

    if form.validate_on_submit():
        print("Formulario válido")

        name= form.name.data.lower()
        last_name= form.last_name.data.lower()
        dob= form.date_of_birth.data
        gender= form.gender.data
        files= form.file_upload.data
        # print(f"Archivos subidos: {form.file_upload.data}")

        athlete_df= pd.DataFrame([
            dict(
                name=name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender)]
        ) 

        for file in files:
            print(file.filename)

        filepaths= []
        for file in files:
            filename= secure_filename(file.filename)

            with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
                file.save(tmp)
                filepath= tmp.name

                filepaths.append(filepath)

        if filepaths:
            process_batch(filepaths, athlete_df)

            flash("Success", "success")
            return redirect(url_for("main.index"))
        else:
            flash("No files in filepaths", "danger")

    return render_template("index.html", form= form)

### RESULTS ###

@main.route("/results", methods=["GET"])
@login_required
def results():
    
        

    return render_template("results.html", prediction = prediction) 

### LOGOUT ###

@main.route("/logout")
@login_required


def logout():
    """Close session and redirect to /login"""

    session.pop("user_id", None)
    return redirect(url_for("main.login"))


