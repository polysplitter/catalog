#!/usr/bin/env python3

from flask import Flask, Blueprint, request, render_template, \
                  session, redirect, url_for, flash, abort

from app import db
from app.wrappers import login_required, validate_catagory

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'edit', set its prefix: app.url/catagory
mod_edit_catagory = Blueprint('edit', __name__, url_prefix='/catagory')


# edit catalog
@mod_edit_catagory.route('/<int:catagory_id>/edit', methods=['POST'])
@login_required()
@validate_catagory()
def edit_catagory(catagory_id):
    """edit catagory"""

    name = request.form.get('name')
    guest_id = session['guest_id']
    exists = db.session.query(Catalogs).filter_by(name=name,
                                                  guest_id=guest_id).scalar()
    if exists:
        return abort(404)

    if name == '':
        return redirect(url_for('home.home'))

    catagory = db.session.query(Catalogs).filter_by(id=catagory_id).one()
    oldname = catagory.name
    catagory.name = name
    db.session.add(catagory)
    db.session.commit()
    flash(f"Catagory {oldname} has been updated to {catagory.name}")

    return redirect(url_for('home.home'))
