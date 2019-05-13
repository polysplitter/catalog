#!/usr/bin/env python3

import datetime
from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db
from app.wrappers import login_required

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'home', set its prefix: app.url/
mod_home = Blueprint('home', __name__, url_prefix='/')


# read catalog request
@mod_home.route('/', methods=['GET'])
@login_required()
def home():
    """get the home page"""

    catagories = db.session.query(Catalogs).all()
    now = datetime.datetime.now()
    return render_template('home/home.html', catagories=catagories, now=now, session=session)
