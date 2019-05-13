
from functools import wraps

from flask import session, redirect, url_for, abort, session
from app import db
from app.models.Catalogs import Catalogs
from app.models.Item import Item


def login_required(catagory_id=None, item_id=None):
    def decorator(func):
        @wraps(func)
        def login_required_wrapper(*args, **kwargs):
            if "username" not in session:
                return redirect(url_for('login.show_login'))
            else:
                return func(*args, **kwargs)
        return login_required_wrapper
    return decorator


def validate_catagory(catagory_id=None):
    def decorator(func):
        @wraps(func)
        def validate_catagory_wrapper(*args, **kwargs):
            catagory_id = kwargs['catagory_id']
            catagory = db.session.query(Catalogs).filter_by(id=catagory_id).one_or_none()
            if catagory is None:
                return abort(404)
            else:
                return func(*args, **kwargs)
        return validate_catagory_wrapper
    return decorator


def validate_items(catagory_id=None, item_id=None):
    def decorator(func):
        @wraps(func)
        def validate_catagory_wrapper(*args, **kwargs):
            catagory_id = kwargs['catagory_id']
            item_id = kwargs['item_id']
            catagory = db.session.query(Catalogs).filter_by(id=catagory_id).one_or_none()
            item = db.session.query(Item).filter_by(id=item_id).one_or_none()
            if catagory is None and item is None:
                return abort(404)
            else:
                return func(*args, **kwargs)
        return validate_catagory_wrapper
    return decorator

