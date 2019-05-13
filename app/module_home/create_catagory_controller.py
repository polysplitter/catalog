#!/usr/bin/env python3

from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db
from app.wrappers import login_required

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'create', set its prefix: app.url/catagory
mod_create_catagory = Blueprint('create', __name__, url_prefix='/catagory')


# create catalog
@mod_create_catagory.route('/create', methods=['POST'])
@login_required()
def create_catagory():
    """create a new catagory"""

    name = request.form.get('name')
    guest_id = session['guest_id']
    exists = db.session.query(Catalogs).filter_by(name=name,
                                               guest_id=guest_id).scalar()
    if exists:
        return redirect(url_for('home.home'))

    if name == '':
        return redirect(url_for('home.home'))

    new_catalog = Catalogs(name=name,
                           guest_id=session['guest_id'])
    db.session.add(new_catalog)
    db.session.commit()
    return redirect(url_for('home.home'))
