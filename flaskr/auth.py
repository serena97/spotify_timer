from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from urllib.parse import urlencode
from random import choice
from string import ascii_uppercase, digits
from flask_cors import CORS
from base64 import b64encode
import requests
import os
from flask import current_app

bp = Blueprint('auth', __name__, url_prefix='/auth')

def id_generator(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

@bp.route('/login')
def login():
    authorize_dict = {
      'response_type': 'code',
      'client_id': current_app.config['CLIENT_ID'],
      'scope': 'user-read-private user-read-email user-modify-playback-state user-read-playback-state',
      'redirect_uri': current_app.config['REDIRECT_URL'],
      'state': id_generator(12)
    }
    params = urlencode(authorize_dict)
    url = 'https://accounts.spotify.com/authorize?%s' % params
    return redirect(url)

@bp.route('/callback/<any:code>')
def getTokens(code):
    auth_data = {
      'code': request.args.to_dict()['code'],
      'redirect_uri': current_app.config['REDIRECT_URL'],
      'grant_type': 'authorization_code'
    }
    header = {
      'Authorization': 'Basic ' + b64encode(bytes(current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET'], 'utf-8')).decode('utf-8')
    }
    res = requests.post('https://accounts.spotify.com/api/token',headers=header, data=auth_data)
    access_token = res.json()['access_token'] 
    return render_template('auth/login.html', access_token=access_token)



