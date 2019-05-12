
import functools

from flask import session, redirect, url_for

def login_required(func):
    @functools.wraps(func)
    def login_required_wrapper():
        if "username" not in session:
            return redirect(url_for('login.show_login'))
        else:
            return func()
    return login_required_wrapper