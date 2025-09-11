import re
# import logging
# from datetime import date
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
# from flask_wtf.file import FileAllowed, FileRequired, MultipleFileField

                    ### CUSTOM VALIDATORS ###

def validate_username(form, field):
    if not re.match(r"^[a-zA-ZA0-9_.-]+$",field.data):        
        raise ValidationError("Only letters, numbers, '-', '_' or '.' are allowed.")
        


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



