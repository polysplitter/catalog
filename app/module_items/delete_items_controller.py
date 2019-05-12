from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

from app import db
from app.wrappers import login_required

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Defines the blueprint: 'delete_items', set its prefix: app.url//catagory/<int:catagory_id>/
mod_delete_items = Blueprint('delete_items', __name__, url_prefix='/catagory/<int:catagory_id>/')


# delete item for catalog
@mod_delete_items.route('/items/<int:item_id>/delete',
                        methods=['POST'])
@login_required()
def delete_item(catagory_id, item_id):
    """delete an item from a catagory"""

    item = db.session.query(Item).filter_by(catalog_id=catagory_id,
                                         id=item_id).one()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('read_items.get_items', catagory_id=catagory_id))