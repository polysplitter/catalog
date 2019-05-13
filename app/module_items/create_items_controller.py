#!/usr/bin/env python3

from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db
from app.wrappers import login_required

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'create_items', set its prefix: app.url//catagory/<int:catagory_id>/
mod_create_items = Blueprint('create_items', __name__, url_prefix='/catagory/<int:catagory_id>/')


# create item for catalog
@mod_create_items.route('/items/create', methods=['POST'])
@login_required()
def create_item(catagory_id):
    """create a new item for a catagory"""

    name = request.form.get('name')
    description = request.form.get('description')

    if name == '' or description == '':
        return redirect(url_for('read_items.get_items', catagory_id=catagory_id))

    item = Item(name=name,
                description=description,
                catalog_id=catagory_id,
                guest_id=session['guest_id'])

    db.session.add(item)
    db.session.commit()

    return redirect(url_for('read_items.get_items', catagory_id=catagory_id))