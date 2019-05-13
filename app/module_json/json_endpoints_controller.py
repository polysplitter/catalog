#!/usr/bin/env python3

from flask import Flask, Blueprint, request, render_template, \
                  session, redirect, url_for, jsonify

from app import db
from app.wrappers import login_required

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# blueprint: 'json', prefix: app.url//catagory/<int:catagory_id>/
mod_json_endpoints = Blueprint('json',
                               __name__,
                               url_prefix='/catagories/')


# json get all catagories
@mod_json_endpoints.route('/JSON')
def get_all_catagories():
    catagories = db.session.query(Catalogs).all()
    return jsonify(Catalogs=[c.serialize for c in catagories])


# json get all items
@mod_json_endpoints.route('/items/JSON')
def get_all_items():
    items = db.session.query(Item).all()
    return jsonify(Item=[i.serialize for i in items])


# json get all items for a catagory
@mod_json_endpoints.route('/<int:catagory_id>/items/JSON')
def get_all_items_for_catagory(catagory_id):
    items = db.session.query(Item).filter_by(catalog_id=catagory_id).all()
    return jsonify(Item=[i.serialize for i in items])
