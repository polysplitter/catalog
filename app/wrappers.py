
import functools

from flask import session, redirect, url_for
from app import db
from app.models.Catalogs import Catalogs

def login_required(required_fields=None):
    def decorator(func):
        @functools.wraps(func)
        def login_required_wrapper(*args, **kwargs):
            if "username" not in session:
                return redirect(url_for('login.show_login'))
            else:
                return func(*args, **kwargs)
        return login_required_wrapper
    return decorator

def validate_catagory(catagory_id):
    def decorator(func):
        @functools.wraps(func)
        def validate_catagory_wrapper(*args):
            catagory = db.session.query(Catalogs).filter_by(id=catagory_id).one_or_none()
            if catagory is None:
                return "404"
            else:
                return func()
        return validate_catagory_wrapper
    return decorator

