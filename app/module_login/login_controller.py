#!/usr/bin/env python3

import random
import string
from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db

from app.models.Guest import Guest

from app.module_login.disconnect import Disconnect
from app.module_login.login import Connect

# Defines the blueprint: 'login', set its prefix: app.url/login
mod_login = Blueprint('login', __name__, url_prefix='/login')

# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@mod_login.route('/')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state
    return render_template('login/login.html', STATE=state)


@mod_login.route('/gconnect', methods=['POST'])
def gconnect():
    """login with google"""
    session = Connect()
    return render_template("login/welcome.html",
                           image=session['picture'],
                           name=session['username'])


# DISCONNECT - Revoke a current user's token and reset their login_session.
@mod_login.route('/gdisconnect')
def gdisconnect():
    """diconnect from google"""
    Disconnect()
    return redirect(url_for("login.show_login"))
