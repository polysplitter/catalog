from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db
from app.wrappers import login_required, validate_items

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
#!/usr/bin/env python3

from app.models.Item import Item

# Defines the blueprint: 'edit_items', set its prefix: app.url//catagory/<int:catagory_id>/
mod_edit_items = Blueprint('edit_items', __name__, url_prefix='/catagory/<int:catagory_id>/')


# update item for catalog
@mod_edit_items.route('/items/<int:item_id>/edit',
           methods=['POST'])
@login_required()
@validate_items()
def edit_item(catagory_id, item_id):
    """edit an item for a catagory"""

    item = db.session.query(Item).filter_by(catalog_id=catagory_id,
                                         id=item_id).one()
    name = request.form.get('name')
    item.name = name
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('read_items.get_items', catagory_id=catagory_id))
