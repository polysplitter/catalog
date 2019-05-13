#!/usr/bin/env python3

from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db
from app.wrappers import login_required

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'read_items', set its prefix: app.url//catagory/<int:catagory_id>/
mod_read_items = Blueprint('read_items', __name__, url_prefix='/catagory/<int:catagory_id>/')


# read item for catalog
@mod_read_items.route('/items', methods=['GET'])
@login_required()
def get_items(catagory_id):
    """get a catagories items"""

    catagory = db.session.query(Catalogs).filter_by(id=catagory_id).one()
    items = db.session.query(Item).filter_by(catalog_id=catagory_id).all()
    return render_template('items/items.html', catagory=catagory, items=items, session=session)
