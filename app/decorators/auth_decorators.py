from functools import wraps

from flask import session, url_for, flash, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            # flash("Login to access this page", "warning")
            return redirect(url_for("main.login"))
        
        return f(*args, **kwargs)
    
    return decorated_function

