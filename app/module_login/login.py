#!/usr/bin/env python3

# New Imports for login
from flask import session as login_session
from flask import request
from app.models.Guest import Guest

from app import db

# Imports for accepting the glogin
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

client_id = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']

GOOGLEAPI = "https://www.googleapis.com/oauth2/v1"
GOOGLEACCOUNTS = "https://accounts.google.com/o/oauth2"


def Connect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
                                 'Failed to upgrade the authorization code.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    login_session['access_token'] = access_token
    url = (f"{GOOGLEAPI}/tokeninfo?access_token={access_token}")
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != client_id:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Get user info
    userinfo_url = f"{GOOGLEAPI}/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    guest_id = getUserId(login_session['email'])
    if not guest_id:
        guest_id = createUser(login_session)
    login_session['guest_id'] = guest_id
    return login_session


def getUserId(email):
    try:
        guest = db.session.query(Guest).filter_by(email=email).one()
        return guest.id
    except Exception:
        return None


def createUser(login_session):
    new_guest = Guest(name=login_session['username'],
                      email=login_session['email'],
                      picture=login_session['picture'])
    db.session.add(new_guest)
    db.session.commit()
    user = db.session.query(Guest).filter_by(email=login_session['email']).one()
    return user.id
