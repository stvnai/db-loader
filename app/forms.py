import re
from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Length, Email, ValidationError
from flask_wtf.file import MultipleFileField, FileAllowed, FileRequired 

                    ### CUSTOM VALIDATORS ###

def validate_username(form, field):
    if not re.match(r"^[a-zA-ZA0-9_.-]+$",field.data):
        raise ValidationError("Only letters, numbers, '-', '_' or '.' are allowed.")

def validate_date(form, field):
    date_of_birth= field.data
    today= date.today()

    if date_of_birth > today:
        raise ValidationError("Invalid date of birth.")
    
    min_birth_date= date(today.year - 12, today.month, today.day)

    if date_of_birth > min_birth_date:
        raise ValidationError("Young athletes should be playing, not training.")
    max_birth_date= date(today.year - 85, today.month, today.day)

    if date_of_birth < max_birth_date:
        raise ValidationError("Rest soldier, forget numbers and enjoy rides.")

                    ### DATA FIELDS ###


class InputForm(FlaskForm):
    
    name= StringField(
        "name",
        validators= [
            InputRequired(),
            Length(max=75)
        ]
    )
    
    last_name= StringField(
        "lastname",
        validators= [
            InputRequired(),
            Length(max=75)
        ]
    )
    
    gender= SelectField(
        "gender",
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("transwoman", "Trans woman"),
            ("transman", "Trans man"),
        ],

        validators= [
            InputRequired()
        ]
    )

    date_of_birth= DateField(
        "dateofbirth",
        validators=[
            InputRequired(),
            validate_date

        ]
    )
    file_upload= MultipleFileField(
        "Select .fit Files",
        validators= [
            FileAllowed(["fit", "FIT"], ".fit files only."),
            FileRequired()
        ]
    )

    submit= SubmitField("upload")


        ### LOGIN FIELDS ###


class LoginForm(FlaskForm):
    username= StringField(
        "username",
        validators= [
            InputRequired(),
            Length(max=150),
            validate_username
        ]
    )
            

    password= PasswordField(
        "password",
        validators= [
            InputRequired(),
            Length(max=50)
        ]
    )

    submit_user= SubmitField("Sign In")



