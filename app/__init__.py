#!/usr/bin/env python3

# Import flask and template operators
from flask import Flask, render_template, session

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# required to pull this after app and db have been created.
from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Import a module / component using its blueprint handler variable (mod_auth)
from app.module_login.login_controller import mod_login
from app.module_home.home_controller import mod_home
from app.module_home.create_catagory_controller import mod_create_catagory
from app.module_home.edit_catagory_controller import mod_edit_catagory
from app.module_home.delete_catagory_controller import mod_delete_catagory
from app.module_items.read_items_controller import mod_read_items
from app.module_items.create_items_controller import mod_create_items
from app.module_items.edit_items_controller import mod_edit_items
from app.module_items.delete_items_controller import mod_delete_items

# Register blueprint(s)
app.register_blueprint(mod_login)
app.register_blueprint(mod_home)
app.register_blueprint(mod_create_catagory)
app.register_blueprint(mod_edit_catagory)
app.register_blueprint(mod_delete_catagory)
app.register_blueprint(mod_read_items)
app.register_blueprint(mod_create_items)
app.register_blueprint(mod_edit_items)
app.register_blueprint(mod_delete_items)


# jinja env filters
def item_count(value):
    count = db.session.query(Item).filter_by(catalog_id=value).count()
    return count


def account(value):
    if value not in session:
        return 'Hello, please log in.'
    return session[value]


def latest_items(value):
    items = db.session.query(Item).order_by(desc(Item.created_time)).limit(5)
    return items


def get_catagory(value):
    catagory = db.session.query(Catalogs).filter_by(id=value).one()
    return catagory.name


def datetimeformat(value):
    return value.strftime('%Y-%m-%d')


app.jinja_env.filters['count'] = item_count
app.jinja_env.filters['account'] = account
app.jinja_env.filters['latest_items'] = latest_items
app.jinja_env.filters['catagory'] = get_catagory
app.jinja_env.filters['datetime'] = datetimeformat

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
