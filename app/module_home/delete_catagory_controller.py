#!/usr/bin/env python3

from flask import Flask, Blueprint, request, render_template, \
                  session, redirect, url_for, flash

from app import db
from app.wrappers import login_required, validate_catagory

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'delete', set its prefix: app.url/catagory
mod_delete_catagory = Blueprint('delete', __name__, url_prefix='/catagory')


# delete catalog
@mod_delete_catagory.route('/<int:catagory_id>/delete', methods=['POST'])
@login_required()
@validate_catagory()
def delete_catagory(catagory_id):
    """delete catagory"""

    catagory = db.session.query(Catalogs).filter_by(id=catagory_id).one()
    items = db.session.query(Item).filter_by(catalog_id=catagory_id).all()
    for item in items:
        flash(f"{item.name} item has been deleted")
        db.session.delete(item)
        db.session.commit()

    name = catagory.name
    db.session.delete(catagory)
    db.session.commit()
    flash(f"Catagory {name} has been deleted")

    return redirect(url_for('home.home'))
