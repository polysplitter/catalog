#!/usr/bin/env python3

import httplib2
import json
from flask import make_response, redirect, url_for, session
import requests

GOOGLEACCOUNTS = "https://accounts.google.com/o/oauth2"


def Disconnect():
        # Only disconnect a connected user.
    access_token = session.get('access_token')
    if access_token is None:
        print('Access Token is empty.')
        response = make_response(
            json.dumps("Current user not connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print("access token is %s" % access_token)
    url = f"{GOOGLEACCOUNTS}/revoke?token={session['access_token']}"
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del session['access_token']
        del session['guest_id']
        del session['username']
        del session['email']
        del session['picture']

        return session
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
