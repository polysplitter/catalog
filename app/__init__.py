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

from app.models.Guest import Guest
from app.models.Catalogs import Catalogs
from app.models.Item import Item


# Import a module / component using its blueprint handler variable (mod_auth)
from app.module_login.login_controller import mod_login as login_module
from app.module_home.home_controller import mod_home as home_module

# Register blueprint(s)
app.register_blueprint(login_module)
app.register_blueprint(home_module)


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